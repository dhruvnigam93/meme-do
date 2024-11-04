from home_components import section_header
from memedo.ai_agents.meme_agent import generate_meme_content
from memedo.ai_agents.summary_agent import get_match_summary
from memedo.models.meme_template import all_memes
from loguru import logger
import json
from fasthtml.common import *
import os, uvicorn
from PIL import Image

BASE_IMAGE_PATH = 'memedo/out/creations/'

# Configure loguru
logger.remove()  # Remove the default logger
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
# logger.add("file_{time}.log", rotation="1 day", level="DEBUG")

# Example usage
logger.info("Logging is set up.")


# Function to extract meme information
def get_meme_info(meme_class):
    meme_instance = meme_class()
    return {
        'id': meme_class.id,
        'name': meme_class.name,
        'description': meme_class.description,
        'instruction': meme_instance.instruction.strip(),
    }


# Collect meme information
memes_info = [get_meme_info(meme["class"]) for meme in all_memes]


#
# @app.post("/generate-images/")
# async \
def generate_images(prompt: str) -> List[str]:
    logger.info(f"Generating images for prompt: {prompt}")
    match_summary = get_match_summary(prompt)
    logger.info(f"Match summary: {match_summary}")
    generated_memes = generate_meme_content(match_summary, memes_info, 5)['memes']
    logger.info(f"Generated memes: {generated_memes}")
    created_memes = []
    for meme_out in generated_memes:
        # instantiate the meme by taking approporiate class from al lmemes using id
        meme_class = next(meme["class"] for meme in all_memes if meme["id"] == meme_out["id"])
        meme_instance = meme_class()
        print(meme_out)
        created_memes.append(meme_instance.create(json.loads(meme_out["meme_creation_input"])))

    generated_images = [f"{BASE_IMAGE_PATH}{x}" for x in created_memes]
    return generated_images


# print(generate_images("india new zealand test match 17 october 2024"))

# gens database for storing generated image details
tables = database('data/gens.db').t
gens = tables.gens
if not gens in tables:
    gens.create(prompt=str, id=int, paths=list, pk='id')
Generation = gens.dataclass()

# Flexbox CSS (http://flexboxgrid.com/)
gridlink = Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css")
app_css = Link(rel="stylesheet", href="app.css", type="text/css")
# Our FastHTML app
app = FastHTML(hdrs=(
    picolink,
    gridlink,
    app_css
))


# Main page
@app.get("/")
def home():
    inp = Input(id="new-prompt", name="prompt", placeholder="Enter a prompt")
    add = Form(Group(inp, Button("Generate")), hx_post="/", target_id='gen-list', hx_swap="afterbegin")
    gen_containers = [generation_preview(g) for g in gens(limit=10)]  # Start with last 10
    gen_list = Div(*reversed(gen_containers), id='gen-list', cls="row")  # flexbox container: class = row
    return Title('Meme Do'), Main(section_header(
                "MEME IS IN THE AIR", "Search about your favourite match and get memes",
                "Create custom viral memes instantly",
                max_width=21, center=False), add, gen_list, cls='container')


# Show the image (if available) and prompt for a generation
def generation_preview(g):
    grid_cls = "row justify-content-md-center"
    image_paths = json.loads(g.paths)
    if len(image_paths) > 0:
        images = [Img(src=image_path, alt="Card image", cls="card-img-top padding-10 img-max") for image_path in image_paths]
        return Div(Card(*images,
                        Div(P(B("Prompt: "), g.prompt, cls="card-text margin-top-20 margin-left-20"), cls=grid_cls),
                        ), id=f'gen-{g.id}', cls=grid_cls)
    return Div(Card(Img(src="memedo/ui-assets/jake-cooking.gif", cls="card-img-top")),
               Div(P(B('Cooking Memes For You!! Please have patience...')), cls="card-text margin-top-20 margin-left-20"),
               id=f'gen-{g.id}', hx_get=f"/gens/{g.id}",
               hx_trigger="every 2s", hx_swap="outerHTML", cls=grid_cls)


# A pending preview keeps polling this route until we return the image preview
@app.get("/gens/{id}")
def preview(id: int):
    print(gens.get(id))
    return generation_preview(gens.get(id))


# For images, CSS, etc.
@app.get("/{fname:path}.{ext:static}")
def static(fname: str, ext: str): return FileResponse(f'{fname}.{ext}')


# Generation route
@app.post("/")
def post(prompt: str):
    clear_input = Input(id="new-prompt", name="prompt", placeholder="Enter a prompt", hx_swap_oob='true')
    if len(prompt) > 3:
        g = gens.insert(Generation(prompt=prompt, paths=[]))
        generate_and_save(prompt, g.id)
        return generation_preview(g), clear_input
    return clear_input


# Generate an image and save it to the folder (in a separate thread)
@threaded
def generate_and_save(prompt: str, id: int):
    # paths = ['memedo/out/creations/20241018011430141900.jpg', 'memedo/out/creations/20241018011430169624.jpg',
    #          'memedo/out/creations/20241018011430313254.jpg', 'memedo/out/creations/20241018011430329335.jpg',
    #          'memedo/out/creations/20241018011430421782.jpg']
    paths = generate_images(prompt)
    print(f"Generated paths: {paths}")
    image_path = paths[0]
    gens.update(Generation(id=id, paths=paths))

    Image.open(image_path)
    return True


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=int(os.getenv("PORT", default=5000)))
