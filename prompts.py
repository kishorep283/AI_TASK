def get_greeting():
    return """ Hello! I'm TalentScout AI, your automated hiring assistant. 

I'll guide you through our initial screening process with a few quick questions. 

May I have your full name, please?"""

def get_tech_stack_prompt():
    return """ Please list the technologies you're proficient in (comma-separated):

Example: 
Python, JavaScript, React, Node.js, PostgreSQL, AWS

Your tech stack:"""

def generate_technical_questions(tech_stack):
    questions = [" Here are some technical questions based on your skills:"]
    
    for tech in tech_stack:
        questions.append(f"\n **{tech}** Questions:")
        questions.append(f"1. What are the key features of {tech}?")
        questions.append(f"2. Can you describe a project where you used {tech}?")
        questions.append(f"3. What are some limitations or challenges with {tech}?")
        questions.append(f"4. How would you optimize a {tech} application?")
    
    questions.append("\nPlease answer these to the best of your ability.")
    return "\n".join(questions)

def get_conclusion():
    return """ Thank you for completing the initial screening!

Our recruiters will review your information and contact you within 3 business days.

You may now close this window or type 'exit' to end the session.

Have a great day! """