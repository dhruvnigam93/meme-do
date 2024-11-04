import datetime
import textwrap

from PIL import Image
from memedo.utils.image_processor import Image_Manager
import os
from PIL import ImageDraw, ImageFont
import imageio


class BaseMemeTemplate:
    id = None
    name = None
    description = None

    template_image_dir = "memedo/static/images/meme_templates"
    output_image_dir = "memedo/out/creations"

    def __init__(self):
        self.instruction = ""
        self.extension = ""

    def create(self, meme_text):
        raise NotImplementedError("Subclasses must implement the create method.")

    def get_template_image(self):
        template_path = f"{self.template_image_dir}/{self.name.lower()}.{self.extension}"
        return Image.open(template_path).convert("RGBA")

    def save_output_image(self, image):
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        image_name = f"{date_str}.jpg"
        file_location = f"{self.output_image_dir}/{image_name}"
        image.save(file_location)
        return image_name

    def add_watermark(self, base_image, text="memedo.ai", position=(10, 10), font_size=20, text_color="white"):
        watermark = Image_Manager.add_text(
            base=base_image,
            text=text,
            position=position,
            font_size=font_size,
            text_color=text_color,
        )
        return Image.alpha_composite(base_image, watermark)


class BaseGIFTemplate:
    id = None
    name = None
    description = None

    template_gif_dir = "memedo/static/images/meme_templates"
    template_output_gif_dir = "memedo/out/creations"
    font_path = "memedo/static/fonts/Arial.ttf"

    def __init__(self, ):
        self.font_path = self.font_path
        self.extension = ""
        self.instruction = ""

    def get_template_gif(self):
        gif_path = f"{self.template_gif_dir}/{self.name.lower()}.{self.extension}"
        return imageio.get_reader(gif_path)

    def add_text_to_frame(self, frame, text, position=(600, 10), font_size=25, text_color="black"):
        # Convert frame to RGBA
        frame = frame.convert("RGBA")

        # Create a drawing context
        draw = ImageDraw.Draw(frame)

        # Load the font
        font = ImageFont.truetype(self.font_path, font_size)

        # Define the maximum width for the text
        max_width = frame.size[0] - position[0] - 10  # Subtracting 10 for padding

        # Wrap the text
        lines = self.wrap_text(text, font, max_width)

        # Draw each line of text
        y_offset = 0
        # Calculate line height
        bbox = font.getbbox('Ay')
        line_height = bbox[3] - bbox[1] + 5  # Adding 5 for line spacing
        for line in lines:
            draw.text((position[0], position[1] + y_offset), line, fill=text_color, font=font)
            y_offset += line_height

        return frame

    def wrap_text(self, text, font, max_width):
        lines = []
        # Use textwrap to split the text into chunks
        for line in text.split('\n'):
            # Wrap the line and add it to the lines list
            lines.extend(textwrap.wrap(line, width=40))  # Adjust width as needed

        # Now adjust each line to fit within max_width
        adjusted_lines = []
        for line in lines:
            words = line.split()
            current_line = ''
            for word in words:
                test_line = current_line + (word + ' ')
                # Get the width of the test_line
                bbox = font.getbbox(test_line)
                text_width = bbox[2] - bbox[0]
                if text_width <= max_width:
                    current_line = test_line
                else:
                    adjusted_lines.append(current_line.rstrip())
                    current_line = word + ' '
            adjusted_lines.append(current_line.rstrip())
        return adjusted_lines

    def save_output_gif(self, frames):
        os.makedirs(f"{self.template_output_gif_dir}", exist_ok=True)
        date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        gif_name = f"{date_str}.gif"
        output_gif_path = f"{self.template_output_gif_dir}/{gif_name}"
        frames[0].save(output_gif_path, save_all=True, append_images=frames[1:], loop=0)
        # imageio.mimsave(output_gif_path, frames)
        return gif_name


class Angry_Jethalal_Beating_Goli(BaseGIFTemplate):
    id = 29
    name = "Angry_Jethalal_Beating_Goli"
    description = "Person A beating Person B for his silly mistake"

    def __init__(self):
        super().__init__()
        self.extension = "gif"
        self.instruction = """ Here are a few examples of input output
###
context:Ind vs Aus ODI big match. India lost some early wickets. Hardik Pandya went to bat and got out on the very first ball. He was expected to play a big inning but got out playing silly big shot and got caught. 
meme_creation_input:{"depiction":"Scenes in dressing room."}
###
context:There was match between FC Barcelona and Real Madrid. Araujo of FC Barcelona was naive and silly and made a foul on Bellingham which resulted in him getting a red card and eventually a lose for FC Barcelona. It was a very silly decision by Araujo.  
meme_creation_input:{"depiction":"Scenes in post match talk between Araujo and coach"}
###
context:There was a educational drive to reduce cases of organization secrets being leaked by using plain text passwords. CTO had repeatly warned a specific employee to not repeat this mistake. But employee was careless and did it again.
meme_creation_input:{"depiction":"Scenes in review meeting"}
###
context:Ved Prakash is a highly always high indiividual. He was warned by his friends to not to smoke weed before the match. But he did it again and got caught by the police.
meme_creation_input:{"depiction":"Scenes in police station"}
###
"""

    def create(self, meme_text):
        reader = self.get_template_gif()
        frames = []

        for frame in reader:
            pil_frame = Image.fromarray(frame)
            modified_frame = self.add_text_to_frame(pil_frame, meme_text["depiction"], position=(50,250), font_size=30,
                                                    text_color='white')
            frames.append(modified_frame)
        gif_name = self.save_output_gif(frames)
        return gif_name


class Change_My_Mind(BaseMemeTemplate):
    id = 10
    name = "Change_My_Mind"
    description = "This is the way it is in my opinion"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
        
###
context:Chocolate chip cookies are the best cookies. Try to change my mind.
meme_creation_input:{"opinion":"Chocolate chip cookies are the best cookies."}
###
context:Learning to code is one of the most rewarding experiences. Change my mind.
meme_creation_input:{"opinion":"Learning to code is one of the most rewarding experiences."}
###
context:Daft Punk is the greatest electronic band to ever exist and you cant convince me otherwise.
meme_creation_input:{"opinion":"Daft Punk is the greatest electronic band to ever exist."}
###
context:In my opinion, the best way to get a good grade in school is to study hard.
meme_creation_input:{"opinion":"The best way to get a good grade in school is to study hard."}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["opinion"],
            position=(500, 385),
            font_size=30,
            text_color="black",
            rotate_degrees=20,
            wrapped_width=22,
        )
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


class Equal(BaseMemeTemplate):
    id = 12
    name = "Equal"
    description = "something is the same as something else"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
###
context:Tea and coffee are equally good. They both make me happy
meme_creation_input:{"first":"Tea", "second":"coffee"}
###
context:Both Dr. Dre and Kanye are amazing. I love them both
meme_creation_input:{"first":"Dr. Dre", "second":"Kanye"}
###
context:If I had to decide between Honda and Tesla I couldnt. They are both great.
meme_creation_input:{"first":"Honda", "second":"Tesla"}
###
context:Riding a bike on dirt is just as fun as riding on the street
meme_creation_input:{"first":"riding a bike on the dirt","second":"riding a bike on the street"}
###
context:Surfing in warm water is the same as surfing in cold water. They are equally fun
meme_creation_input:{"first":"surfing in cold water","second":"surfing in warm water"}
###
context:alsdjkfa
meme_creation_input:{"first":"alsdjkfa","second":"alsdjkfa"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image_1 = Image_Manager.add_text(
            base=base,
            text=meme_text["first"],
            position=(70, 180),
            font_size=45,
            wrapped_width=12,
            rotate_degrees=345,
        )
        overlay_image_2 = Image_Manager.add_text(
            base=base,
            text=meme_text["second"],
            position=(575, 100),
            font_size=45,
            wrapped_width=12,
            rotate_degrees=345,
        )
        base = Image.alpha_composite(base, overlay_image_1)
        base = Image.alpha_composite(base, overlay_image_2)
        image_name = self.save_output_image(base)
        return image_name


class Buff_Doge_Vs_Cheems(BaseMemeTemplate):
    id = 14
    name = "Buff_Doge_vs_cheems"
    description = "when someone is strong in one area but comically weak in another"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
###
context:Jim does well in the gym, but he is a small whimpering figure in front of his crush
meme_creation_input:{"strong":"Jim in the gym", "weak":"JIm in fron of crush"}
###
context:THe lakers do well at home but fail misrably away from hom
meme_creation_input:{"strong":"Lakers at home", "weak":"Lakers away from home"}
###
context:The australian team is strong in the field but weak in bowling
meme_creation_input:{"strong":"Australian team when fielding", "weak":"Australian team when bowling"}
###
context:In the first half manchester united were very stong and had most of the possession but in the second half they were weak and conceded a goal
meme_creation_input:{"strong":"Manchester united in the first half", "weak":"Manchester united in the second half"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image_1 = Image_Manager.add_text(
            base=base,
            text=meme_text["strong"],
            position=(70, 180),
            font_size=45,
            wrapped_width=12,
            rotate_degrees=345,
        )
        overlay_image_2 = Image_Manager.add_text(
            base=base,
            text=meme_text["weak"],
            position=(575, 100),
            font_size=45,
            wrapped_width=12,
            rotate_degrees=345,
        )
        base = Image.alpha_composite(base, overlay_image_1)
        base = Image.alpha_composite(base, overlay_image_2)
        image_name = self.save_output_image(base)
        return image_name


class Indifferent(BaseMemeTemplate):
    id = 2
    name = "Indifferent"
    description = "here is a guys who iburning a fact that he does not want to acknowledge because it is too painful"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
###
context:Doesnt matter that people might elect someone stupid that will affect us all
meme_creation_input:{"action":"People might elect someone stupid"}
###
context:You will never be good enough to beat the indian cricket team
meme_creation_input:{"action":"You will never be good enough to beat the indian cricket team"}
###
context:Mavericks are unbeatable at their home ground. 
meme_creation_input:{"action":"Mavericks are unbeatable at their home ground"}
###
context:In dian fans realize that You will nver have a team with good bowlers
meme_creation_input:{"action":"You will nver have a team with good bowlers"}
###
context:We should all wear sunscreen, but some people dont seem to care
meme_creation_input:{"action":"wearing sunscreen"}
###
context:Getting patents is sometimes important, but sometimes it is not at all
meme_creation_input:{"action":"Getting patents is sometimes important"}
###
context:Make sure to always write tests before writing code
meme_creation_input:{"action":"writing tests before writing code"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["action"],
            position=(100, 175),
            font_size=40,
            wrapped_width=11,
        )
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


class Ineffective_Solution(BaseMemeTemplate):
    id = 9
    name = "Ineffective_Solution"
    description = "the solution was a poor way of doing it"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
###
context:There is a bunch of traffic in town. The government decided to make the roads wider, but that's not the problem
meme_creation_input:{"attempted_solution":"more roads", "failure":"traffic"}
###
context:Some people who brush their hair still get messy hair.
meme_creation_input:{"attempted_solution":"brush", "failure":"messy hair"}
###
context:I go for a walk daily, but then I end up eating a donut. Pretty ineffective
meme_creation_input:{"attempted_solution":"walk daily", "failure":"eating a donut"}
###
context:I drink coffee to be more awake, but then I cant sleep and I am tired the next day
meme_creation_input:{"attempted_solution":"drink coffee", "failure":"cant sleep and I am tired the next day"}
###
context:I try to read a book to spend less time on my phone, but I end up googling concepts on my phone
meme_creation_input:{"attempted_solution":"read a book to spend less time on my phone", "failure":"end up googling concepts on my phone"}
###
context:bralkajsd;
meme_creation_input:{"attempted_solution":"bralkajsd;", "failure":"bralkajsd;"}
###
context:I wish AI could help me make memes
meme_creation_input:{"attempted_solution":"AI making memes", "failure":"The memes are beyond my sense of humor"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image_1 = Image_Manager.add_text(
            base=base,
            text=meme_text["attempted_solution"],
            position=(75, 75),
            font_size=50,
            text_color="white",
            wrapped_width=14,
        )
        overlay_image_2 = Image_Manager.add_text(
            base=base,
            text=meme_text["failure"],
            position=(125, 725),
            font_size=50,
            text_color="white",
            wrapped_width=15,
            rotate_degrees=350,
        )
        base = Image.alpha_composite(base, overlay_image_1)
        base = Image.alpha_composite(base, overlay_image_2)
        image_name = self.save_output_image(base)
        return image_name


class No_Responsibility(BaseMemeTemplate):
    id = 8
    name = "No_Responsibility"
    description = "two parties blaming each other for something"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
###
context:THe batting could have samed team A but their bowlers let them down. Dont know who to blame
meme_creation_input:{"party_one":"team a batting", "party_two":"teem a bolwing"}
###
context:The shoemaker blames the sockmaker and the sockmaker blames the shoemaker
meme_creation_input:{"party_one":"shoemaker", "party_two":"sockmaker"}
###
context:Coffee blames tea for not waking me up after I drink both
meme_creation_input:{"party_one":"coffee", "party_two":"tea"}
###
context:I cant do anything useful
meme_creation_input:{"party_one":"me", "party_two":"me"}
###
context:break
meme_creation_input:{"party_one":"break", "party_two":"break"}
meme_creation_input:{"party_one":"break", "party_two":"break"}
###
context:the whole team let the fans down. the defenders and attackers
meme_creation_input:{"party_one":"Team defence", "party_two":"Team attack"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image_1 = Image_Manager.add_text(
            base=base,
            text=meme_text["party_one"],
            position=(175, 200),
            font_size=40,
            text_color="white",
            wrapped_width=12,
        )
        overlay_image_2 = Image_Manager.add_text(
            base=base,
            text=meme_text["party_two"],
            position=(800, 200),
            font_size=40,
            text_color="white",
            wrapped_width=12,
        )
        base = Image.alpha_composite(base, overlay_image_1)
        base = Image.alpha_composite(base, overlay_image_2)
        image_name = self.save_output_image(base)
        return image_name


class Mujhe_Ghar_Jaana_Hai(BaseMemeTemplate):
    id = 23
    name = "Mujhe_Ghar_Jaana_Hai"
    description = "Somebody is clearly traumatized and wants to go home"

    def __init__(self):
        super().__init__()
        self.extension = "png"
        self.instruction = """ Here are a few examples of input output
###
context:The mavericks fanshad a horrible day today. They lost the game badly.
meme_creation_input:{"who":"Mavericks fans"}
###
context: Everything went wrong got John today in the meeting - he just wanted to leave
meme_creation_input:{"who":"John today"}
###
context:THe captain was let down by shames performance today
meme_creation_input:{"who":"the captain today seeing shamis bowling"}
###
context: Frances defenders seeing the speed of messi
meme_creation_input:{"who":"Frances defenders seeing the speed of messi"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["who"],
            position=(100, 115),
            font_size=100,
            wrapped_width=40,
            text_color="white"
        )
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


class Guy_Chilling(BaseMemeTemplate):
    id = 38
    name = "Guy_Chilling"
    description = "Team or player relaxing with confidence"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
        
###
context:India having set a huge target and already have the opponents batsmen bowled out and now rohit sharma the captain is allowing virat kohli to bowl a few overs.
meme_creation_input:{"opinion":"Rohit enjoying virat bowling a few overs."}
###
context:A group of friends are playing a board game, and one person makes a brilliant move to win, but instead of bragging about it, they just smile and say "Good game, everyone."
meme_creation_input:{"opinion":"When you know youre right but dont want to rub it in"}
###
context:A group of coworkers are scrambling to finish a project before a deadline, but one coworker is calmly working away, sipping their coffee and not letting the stress get to them.
meme_creation_input:{"opinion":"Just chillin while everyone else is stressing."}
###
context:A student has just finished an important exam, and they walk out of the classroom with a smile on their face, knowing that they aced it.
meme_creation_input:{"opinion":"The face of someone who knows theyve already won."}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["opinion"],
            position=(50, 450),
            font_size=30,
            text_color="white",
            rotate_degrees=0,
            wrapped_width=40,
        )
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


class Jethalal_Angry(BaseGIFTemplate):
    id = 42
    name = "Jethalal_Angry"
    description = "Someone is really angry with what happened"

    def __init__(self):
        super().__init__()
        self.extension = "gif"
        self.instruction = """ Here are a few examples of input output

###
context:The coach pep has to be angry with his attackets performance today
meme_creation_input:{"who":"Pep looking at his attackers"}
###
context: That was wrong. marcelo was not out and the umpire gave him out. surely is is going to be angry
meme_creation_input:{"who":"Marcello after the umpire gave him out wrongly"}
###
context: that lineup does not make sense. How could the coash not be playing spencer? surely this will hurt the team
meme_creation_input:{"who":"Indian fans after seeing the lineup"}
###
context: The dugout must be getting crazy because hardik was told tp play slow but he is clearly in no mood and is hitting the ball hard
meme_creation_input:{"who":"The dugout after hardik starts hitting the ball hard"}
###
"""

    def create(self, meme_text):
        reader = self.get_template_gif()
        frames = []

        for frame in reader:
            pil_frame = Image.fromarray(frame)
            modified_frame = self.add_text_to_frame(pil_frame, meme_text["who"], position=(50, 300), font_size=30,
                                                    text_color='white')
            frames.append(modified_frame)
        gif_name = self.save_output_gif(frames)
        return gif_name


class Bike_Fall(BaseMemeTemplate):
    id = 13
    name = "Bike_Fall"
    description = "You yourself are the reason for your failure"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
        
###
context: In recent news a School is found to suspend kids who defends himself from bullies rather than suspending the bullies. In interview, it asks people why does everyone hates us?
meme_creation_input:{"first":"We prevent bullying.",  "second": "Suspends kids who defended themselves.", "third": "why does everyone hates us?"}
###
context: India vs new zealand test match. Weather conditions are overcast, windy and rainy. India wins the toss and elects to bat first. India is then all out for mere 46 runs.
meme_creation_input:{"first":"भारत ने टॉस जीता", "second": "भारत ने बादल छाए रहने की स्थिति में पहले बल्लेबाजी करने का फैसला किया", "third":"46 पर ढेर"}
###
context:India vs Sri Lanka test match. India is playing really well and is about to win the match. Just then the set batsmen Rishabh Pant tries to hit a big shot and is caught out. Then whole Indian batting collapses and India loses the match.
meme_creation_input:{"first":"India is playing really well", "second": "Rishabh Pant goes for a biggie and is caught out", "third":"India loses"}
###
context: I was waiting for the weekend to come and had planned to do a lot of things. Saturday comes and I am too tired to do anything. Sunday comes and I am too lazy to do anything. Monday comes and I am too busy to do anything."
meme_creation_input:{"first": "Saturday", "second": "Sunday", "third":"Monday"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image_1 = Image_Manager.add_text(
            base=base,
            text=meme_text["first"],
            position=(250, 100),
            font_size=25,
            text_color="black",
            wrapped_width=20
        )
        overlay_image_2 = Image_Manager.add_text(
            base=base,
            text=meme_text["second"],
            position=(40, 350),
            font_size=25,
            text_color="black",
            wrapped_width=20
        )
        overlay_image_3 = Image_Manager.add_text(
            base=base,
            text=meme_text["third"],
            position=(250, 500),
            font_size=25,
            text_color="black",
            wrapped_width=20
        )
        base = Image.alpha_composite(base, overlay_image_1)
        base = Image.alpha_composite(base, overlay_image_2)
        base = Image.alpha_composite(base, overlay_image_3)
        image_name = self.save_output_image(base)
        return image_name


class Thinking_About_Other_Women(BaseMemeTemplate):
    id = 21
    name = "Thinking_About_Other_Women"
    description = "the man is not talking to his wife because he is thinking. she thinks its about other women, but he is disturbed by other thoughts."

    def __init__(self):
        super().__init__()
        self.extension = "png"
        self.instruction = """ Here are a few examples of input output
        
###
context: India vs New Zealand test match. Virat Kohli got out for a duck in the first innings. He is a very good player and got out for a duck which was unexpected. 
meme_creation_input:{"thoughts":"Why did I pick Virat Kohli for my fantasy team??""}
###
context: Man and woman are sleeping together. Woman is thinking suspicious about man whereas the man is thinking about some food that he had in the evening and is regretting on the decision.
meme_creation_input:{"thoughts":"Why did I eat that entire pizza by myself?"}
###
context: There was match between FC Barcelona and Real Madrid. Araujo of FC Barcelona was naive and silly and made a foul on Bellingham which resulted in him getting a red card and eventually a lose for FC Barcelona. It was a very silly decision by Araujo.  
meme_creation_input:{"thoughts":"Why did Araujo make that silly foul?"}
###
context: There was a match between India and Australia World Cup Final 2023. Rohit Sharma was playing really well and had already hit a six in the over. He then tried to hit another big shot but was caught out. It was a very silly decision by Rohit Sharma. He should have played more carefully.
meme_creation_input:{"thoughts":"Why did Rohit Sharma tried to hit another six?"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["thoughts"],
            position=(650, 15),
            font_size=25,
            text_color="black",
            rotate_degrees=0,
            wrapped_width=20,
        )
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


class Disaster_PakFan(BaseMemeTemplate):
    id = 32
    name = "disappointed-pak-fan"
    description = "This is the face of disappointment when expectations fail."

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input output
        
###
context:Pakistan lost the match.
meme_creation_input:{"opinion":"Pakistan lost the match."}
###
context:You were promised pizza, but all thats left is salad.
meme_creation_input:{"opinion":"You were promised pizza, but all thats left is salad."}
###
context:You spent hours learning to code, but the program still doesn’t work.
meme_creation_input:{"opinion":"You spent hours learning to code, but the program still doesn’t work."}
###
context:Your favorite show was cancelled after the best season.
meme_creation_input:{"opinion":"Your favorite show was cancelled after the best season."}
###
context:In my opinion, the best way to deal with Mondays is to pretend they don’t exist.
meme_creation_input:{"opinion":"The best way to deal with Mondays is to pretend they don’t exist."}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["opinion"],
            position=(120, 385),
            font_size=50,
            text_color="white",
            rotate_degrees=0,
            wrapped_width=40,
        )
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


class Bored(BaseMemeTemplate):
    id = 61  # Assign a unique ID
    name = "sarfaraz-khan-yawning"
    description = "This meme shows a bored or uninterested expression"

    def __init__(self):
        super().__init__()
        self.extension = "jpeg"
        self.instruction = """ Here are a few examples of input-output pairs for this meme template
        
###
context:When the meeting is going on for hours and nothing productive is happening.
meme_creation_input:{"caption":"When the meeting is going on for hours and nothing productive is happening."}
###
context:My reaction when someone explains something I already know.
meme_creation_input:{"caption":"My reaction when someone explains something I already know."}
###
context:When you realize you forgot to charge your phone, and now you are stuck without it.
meme_creation_input:{"caption":"When you realize you forgot to charge your phone, and now you are stuck without it."}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        # Add text for 'caption'
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["caption"],
            position=(10, 50),  # Adjust the position based on where you'd like the text
            font_size=15,
            text_color="black",
            wrapped_width=20,
        )
        # Combine overlays
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


class Confused(BaseMemeTemplate):
    id = 15  # Assign a unique ID
    name = "rohit_conf"
    description = "This meme shows a confused or perplexed expression - when it just goes over your head what happened"

    def __init__(self):
        super().__init__()
        self.extension = "png"
        self.instruction = """ Here are a few examples of input-output pairs for this meme template
        
###
context:When the code runs but you have no idea why it worked.
meme_creation_input:{"caption":"When the code runs but you have no idea why it worked."}
###
context:Trying to figure out why the meeting was called in the first place.
meme_creation_input:{"caption":"Trying to figure out why the meeting was called in the first place."}
###
context:When you thought you understood the assignment, but the results say otherwise.
meme_creation_input:{"caption":"When you thought you understood the assignment, but the results say otherwise."}
###
context: Exceptional performance by alonso but even his 3 goals could not save the team from a loss
meme_creation_input:{"caption":"when you score 3 goals and loose"}
###
context: It is hard to see why the coash would select A over B to go out to play in these conditions
meme_creation_input:{"caption":"fans looking at coach sending A over B"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        # Add text for 'caption'
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["caption"],
            position=(75, 200),  # Adjust based on where the text fits best
            font_size=100,
            text_color="black",
            wrapped_width=30,
        )
        # Combine overlays
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name



class Unintended_Damage(BaseMemeTemplate):
    id = 50 # Assign a unique ID
    name = "mujhe-kyu-toda"
    description = "Used when someone is destroyed and thrashed without it being their fault"

    def __init__(self):
        super().__init__()
        self.extension = "jpeg"
        self.instruction = """ Here are a few examples of input-output pairs for this meme template
        
###
context:When someone spills a drink on your laptop and now it wont turn on.
meme_creation_input:{"who":"My laptop"}
###
context:When you let your friend borrow your car, and they return it with a dent.
meme_creation_input:{"who":"My car"}
###
context:When you innocently bump into the bookshelf, and the whole thing collapses.
meme_creation_input:{"who":"Me"}
###
context:nether lands were peacefully exiting the world cup after defeating the defending champions but then they were thrashed by the India badly who did not even need the win
meme_creation_input:{"who":"Netherlands after the match"}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        # Add text for 'caption'
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["who"],
            position=(10, 150),  # Adjust position as needed
            font_size=15,
            text_color="white",
            wrapped_width=35,
        )
        # Combine overlays
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


class Sad_Pablo(BaseMemeTemplate):
    id = 18  # Assign a unique ID
    name = "Sad-Pablo-Escobar"
    description = "This meme expresses the sadness and boredom associated with anticipation or waiting"

    def __init__(self):
        super().__init__()
        self.extension = "jpg"
        self.instruction = """ Here are a few examples of input-output pairs for this meme template
        
###
context:When you re waiting for your food to arrive but it s been an hour already.
meme_creation_input:{"caption":"When you re waiting for your food to arrive but it s been an hour already."}
###
context:When you send someone a message and they don t respond for hours.
meme_creation_input:{"caption":"When you send someone a message and they don t respond for hours."}
###
context:When the weekend is almost over and you realize you didn t do anything fun.
meme_creation_input:{"caption":"When the weekend is almost over and you realize you didn t do anything fun."}
###
"""

    def create(self, meme_text):
        base = self.get_template_image()
        # Add text for 'caption'
        overlay_image = Image_Manager.add_text(
            base=base,
            text=meme_text["caption"],
            position=(50, 50),  # Adjust position as needed
            font_size=30,
            text_color="white",
            wrapped_width=30,
        )
        # Combine overlays
        base = Image.alpha_composite(base, overlay_image)
        image_name = self.save_output_image(base)
        return image_name


# class Overconfident(BaseMemeTemplate):
#     id = 19  # Assign a unique ID
#     name = "jethalal-overconfident"
#     description = "This meme represents someone being overly confident, often humorously."

#     def __init__(self):
#         super().__init__()
#         self.extension = "gif"  # Assuming we'll extract a frame and save as .jpg
#         self.instruction = """ Here are a few examples of input-output pairs for this meme template

# ###
# context:When you haven't studied but still show up to the exam like you're going to ace it.
# meme_creation_input:{"caption":"When you haven't studied but still show up to the exam like you're going to ace it."}
# ###
# context:When you think you can fix the bug in production without checking the logs.
# meme_creation_input:{"caption":"When you think you can fix the bug in production without checking the logs."}
# ###
# context:When you challenge your friend to a game you’ve never played and still think you’ll win.
# meme_creation_input:{"caption":"When you challenge your friend to a game you’ve never played and still think you’ll win."}
# ###
# """

#     def create(self, meme_text):
#         base = self.get_template_image()
#         # Add text for 'caption'
#         overlay_image = Image_Manager.add_text(
#             base=base,
#             text=meme_text["caption"],
#             position=(50, 50),  # Adjust position as needed
#             font_size=30,
#             text_color="white",
#             wrapped_width=30,
#         )
#         # Combine overlays
#         base = Image.alpha_composite(base, overlay_image)
#         image_name = self.save_output_image(base)
#         return image_name

class Dhol_Rajpal_Yadav(BaseGIFTemplate):
    id = 31
    name = "Dhol_Rajpal_Yadav"
    description = "An overconfident person celebrating the win after doing nothing"

    def __init__(self):
        super().__init__()
        self.extension = "gif"
        self.instruction = """ Here are a few examples of input output
###
context:Ind vs Aus ODI big match. India lost some early wickets. Hardik Pandya went to bat and got out on the very first ball. He was expected to play a big inning but got out playing silly big shot and got caught. 
meme_creation_input:{"depiction":"Hardik Pandya the next day"}
###
context:There was match between FC Barcelona and Real Madrid. Araujo of FC Barcelona was naive and silly and made a foul on Bellingham which resulted in him getting a red card and eventually a lose for FC Barcelona. It was a very silly decision by Araujo.  
meme_creation_input:{"depiction":"Araujo in the press conference after the match"}
###
context:Ind vs South Africa T20 Final match. India won the match after close competition. The players who played well were celebrating. But there was one player yuzvendra chahal who was on bench but was celebrating as if he single handedly won the match.
meme_creation_input:{"depiction":"Yuzvendra Chahal after the match"}
###
context:In office meeting, the team was celebrating success about the new project. There was this manager Ved Prakash of the team who contributed nothing and was yet celebrating like he did all the hard work.
meme_creation_input:{"depiction":"Ved Prakash during the celebration of the new project"}
###
"""

    def create(self, meme_text):
        reader = self.get_template_gif()
        frames = []

        for frame in reader:
            pil_frame = Image.fromarray(frame)
            modified_frame = self.add_text_to_frame(pil_frame, meme_text["depiction"], position=(40, 330), font_size=20,
                                                    text_color='white')
            frames.append(modified_frame)
        gif_name = self.save_output_gif(frames)
        return gif_name

# Define the meme templates
meme_templates = [
    Change_My_Mind,
    Equal,
    Indifferent,
    Ineffective_Solution,
    No_Responsibility,
    Guy_Chilling,
    Bike_Fall,
    Thinking_About_Other_Women,
    Angry_Jethalal_Beating_Goli,
    Disaster_PakFan,
    Bored,
    Confused,
    Unintended_Damage,
    Sad_Pablo,
    Mujhe_Ghar_Jaana_Hai,
    Jethalal_Angry,
    Buff_Doge_Vs_Cheems,
    Dhol_Rajpal_Yadav
]

# Create the final dictionary
all_memes = []
for template in meme_templates:
    all_memes.append({
        "id": template.id,
        "class": template
    })
