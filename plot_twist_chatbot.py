import nltk
from textblob import TextBlob
import re
import random
import json
import os

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class ChatbotBase:
    def __init__(self, name="Chatbot"):
        self.name = name
        self.conversation_is_active = True

    def greeting(self):
        print(f'Hello I am {self.name}')

    def farewell(self):
        print('Goodbye!')
    
    def conversation_is_active(self):
        return self.conversation_is_active

    def receive_input(self):
        return input("> ")

    def process_input(self, user_input):
        raise NotImplementedError('process_input() not implemented')

    def generate_response(self, processed_input):
        raise NotImplementedError('generate_response() not implemented')

    def respond(self, out_message=None):
        if isinstance(out_message, str): 
            print(out_message)

        received_input = self.receive_input()
        
        # Check for quit command first
        if received_input.lower() in ['quit', 'exit', 'bye']:
            self.conversation_is_active = False
            return "Goodbye!"
            
        processed_input = self.process_input(received_input)
        response = self.generate_response(processed_input)
        return response

class PlotTwistChatbot(ChatbotBase):
    def __init__(self, name="Plot Twist Storyteller"):
        super().__init__(name)
        self.story_state = {
            "genre": "adventure",
            "mood": "neutral",
            "characters": [],
            "locations": [],
            "items": [],
            "story_arc": []
        }
        self.conversation_history = []
    
    def greeting(self):
        greeting_msg = """
🎭 Welcome to PLOT TWIST - Your AI Storytelling Companion!

I'll be your Game Master for an interactive adventure. 
Tell me what you want to do, and I'll build the story around your choices.

You can:
- Explore locations (type: 'go to forest', 'enter castle')
- Fight enemies (type: 'attack dragon', 'fight goblin')  
- Find items (type: 'take sword', 'get key')
- Just tell me what you want to do!

Type 'quit' to exit at any time.

Where would you like to begin?
        """
        print(greeting_msg)
    
    def process_input(self, user_input):
        """Process user input using NLP techniques"""
        processed = {
            "raw_text": user_input,
            "sentiment": self.analyze_sentiment(user_input),
            "keywords": self.extract_keywords(user_input),
            "action_type": self.classify_input(user_input)
        }
        
        self.update_story_state(processed)
        self.conversation_history.append(processed)
        return processed
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return "positive"
            elif polarity < -0.1:
                return "negative"
            else:
                return "neutral"
        except:
            return "neutral"
    
    def extract_keywords(self, text):
        """Extract important keywords"""
        story_keywords = [
            'forest', 'castle', 'cave', 'river', 'mountain', 'village', 'town',
            'sword', 'key', 'map', 'treasure', 'gold', 'dragon', 'wizard', 'monster',
            'fight', 'attack', 'run', 'hide', 'explore', 'search', 'look',
            'take', 'get', 'grab', 'open', 'enter', 'go', 'move', 'walk'
        ]
        
        found_keywords = []
        words = re.findall(r'\b\w+\b', text.lower())
        
        for word in words:
            if word in story_keywords:
                found_keywords.append(word)
        
        return list(set(found_keywords))
    
    def classify_input(self, text):
        """Classify the type of user input"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['go', 'move', 'walk', 'enter', 'explore', 'travel']):
            return "movement"
        elif any(word in text_lower for word in ['attack', 'fight', 'kill', 'defeat', 'hit', 'battle']):
            return "combat"
        elif any(word in text_lower for word in ['take', 'get', 'grab', 'pick', 'collect']):
            return "item_interaction"
        elif any(word in text_lower for word in ['talk', 'ask', 'tell', 'say', 'speak']):
            return "dialogue"
        else:
            return "narrative"
    
    def update_story_state(self, processed_input):
        """Update story based on user input"""
        # Update mood
        self.story_state["mood"] = processed_input["sentiment"]
        
        # Add locations and items from keywords
        for keyword in processed_input["keywords"]:
            if keyword in ['forest', 'castle', 'cave', 'river', 'mountain', 'village', 'town']:
                if keyword not in self.story_state["locations"]:
                    self.story_state["locations"].append(keyword)
            elif keyword in ['sword', 'key', 'map', 'treasure', 'gold']:
                if keyword not in self.story_state["items"]:
                    self.story_state["items"].append(keyword)
    
    def generate_response(self, processed_input):
        """Generate story response based on input"""
        # Generate response based on action type
        if processed_input["action_type"] == "movement":
            response = self.generate_movement_response()
        elif processed_input["action_type"] == "combat":
            response = self.generate_combat_response()
        elif processed_input["action_type"] == "item_interaction":
            response = self.generate_item_response()
        else:
            response = self.generate_narrative_response()
        
        # Add tone based on sentiment
        response = self.adjust_tone(response, processed_input["sentiment"])
        
        # Store story progression
        self.story_state["story_arc"].append(response[:100])
        
        return response
    
    def generate_movement_response(self):
        locations = [
            "a dark, ancient forest where sunlight barely penetrates the canopy",
            "a crumbling stone castle atop a misty hill", 
            "a deep, echoing cave that seems to breathe with ancient magic",
            "a rushing river that carves through the landscape",
            "a quiet village with smoke rising from chimneys",
            "a mysterious temple covered in strange symbols"
        ]
        events = [
            "You journey onward and discover",
            "After some time, you arrive at",
            "Your path leads you to",
            "Through the mist, you see"
        ]
        
        return f"{random.choice(events)} {random.choice(locations)}. What would you like to do here?"
    
    def generate_combat_response(self):
        enemies = [
            "a fierce dragon with scales like emeralds",
            "a band of mischievous goblins armed with crude weapons",
            "an ancient stone guardian that awakens at your approach",
            "a shadowy figure that moves like smoke",
            "a giant spider with webs covering the trees"
        ]
        outcomes = [
            "You ready your weapon and face",
            "With courage, you prepare to fight",
            "Combat instincts take over as you confront",
            "You stand your ground against"
        ]
        
        return f"{random.choice(outcomes)} {random.choice(enemies)}. What's your next move?"
    
    def generate_item_response(self):
        items = [
            "a glowing sword that hums with power",
            "an ancient key covered in rust but still sturdy",
            "a mysterious map drawn on aged parchment",
            "a healing potion that shimmers with blue light", 
            "a bag of gold coins that jingles promisingly",
            "a magical amulet with a pulsating gem"
        ]
        discoveries = [
            "You carefully search the area and find",
            "To your surprise, you discover", 
            "Hidden just out of sight is",
            "Your keen eyes spot"
        ]
        
        return f"{random.choice(discoveries)} {random.choice(items)}. This could be useful on your journey!"
    
    def generate_narrative_response(self):
        hooks = [
            "The story takes an unexpected turn...",
            "New possibilities unfold before you...",
            "The plot thickens as mysteries deepen...",
            "Your adventure continues with new challenges..."
        ]
        questions = [
            "What path will you choose next?",
            "How will you shape this chapter of your story?",
            "What discovery awaits you around the next corner?",
            "Where does your curiosity lead you now?"
        ]
        
        return f"{random.choice(hooks)} {random.choice(questions)}"
    
    def adjust_tone(self, response, sentiment):
        """Adjust tone based on sentiment analysis"""
        if sentiment == "positive":
            modifiers = ["Fortunately,", "With renewed hope,", "Happily,", "Brightly,"]
        elif sentiment == "negative":
            modifiers = ["Unfortunately,", "With growing concern,", "Darkly,", "Sadly,"]
        else:
            modifiers = ["Meanwhile,", "As events unfold,", "Curiously,", "Suddenly,"]
        
        if random.random() > 0.6:  # 40% chance to add modifier
            response = f"{random.choice(modifiers)} {response.lower()}"
        
        return response
    
    def farewell(self):
        print("\n" + "="*50)
        print("Thank you for playing Plot Twist!")
        if self.story_state["locations"]:
            print(f"You visited: {', '.join(self.story_state['locations'])}")
        if self.story_state["items"]:
            print(f"You found: {', '.join(self.story_state['items'])}")
        print("Hope to continue your adventure soon!")
        print("="*50)

def main():
    chatbot = PlotTwistChatbot()
    chatbot.greeting()
    
    # Start with an initial prompt
    initial_response = chatbot.generate_response({
        "action_type": "narrative", 
        "sentiment": "neutral",
        "keywords": []
    })
    print(initial_response)
    
    # Main conversation loop
    while chatbot.conversation_is_active:
        try:
            user_input = chatbot.receive_input()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                chatbot.conversation_is_active = False
                break
                
            # Process and respond to user input
            processed = chatbot.process_input(user_input)
            response = chatbot.generate_response(processed)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\nStory interrupted...")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Let's continue the story...")
            response = "What would you like to do next?"
            print(response)
    
    chatbot.farewell()

if __name__ == "__main__":
    main()