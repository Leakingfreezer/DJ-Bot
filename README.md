# DJ BOT 🪩🕺
### Taking advantage of the new Google Python Mediapipe, create and navigate a rave scene inside your room with just your laptop and camera, and utilize a bot agent that uses ROS2 workflow to enhance the atmosphere. 

## Demo Video

## Referenced Resources 
- https://blog.roboflow.com/what-is-mediapipe/ -> used to understand the mediapipe library
- https://medium.com/analytics-vidhya/mediapipe-hand-gesture-based-volume-controller-in-python-w-o-gpu-67db1f30c6ed -> volume controlling inspo
- https://chernando.com/blog/2023/07/23/hand-tracking-for-mouse-input.html -> hand-tracking for mouse input inpso/understanding

## My Background 
Specifically for this project, I think it's important to consider my multidisciplinary tech and music background. I love music, I enjoy manipulating art to create new art, on the side I play with my DJ control deck and launchpad to play with beats. DJing really evokes a 
certain type of vide and emotion that I believe should also be **Seen**, what does that mean? Well, touch designer? I first wanted to create an immersive DJ deck with just my laptop, so I thought of how I could break down the DJ deck functions and translate them to my laptop.
Well there was the trackpad, I could hypothetically section the trackpad into 8 sections and there would be my DJ deck, however, gathering that data was a bit harder than expected and I wanted to play with mediapipe, thats where the magic is! Use my laptop camera, mediapipe
detects my hand and therefore can activate different functions. To give myself more context, in highschool I was an outreach/design member Bearbella FTC robotics team, I aided in outreach communication to businesses, simplified robot logic as a mentor for a FLL camp, and 
designed with CAD. Our bot was specifically known to be modular in design, this meant its' functions where separate from each other and that they ran concurrently by communicating with each other. This design proccess follows me everywhere, to hackathons like Ultrahacks to building
my side projects, as a management engineering student, previous project manager/founder of multiple NGOs, I know how to look at a complex system/goal and pipeline the different workflows and compartments that must work hand in hand to get to the finished product. Mediapipe also called 
my attention as I'm a spatial designer for UW reality labs, designing the interactive vr/rx environment from scratch. I'm learning on the job about UX/UI principles, industry demand iteration workflows, figma, unity and blender. 

Concurrently, I planning the co-designing of a AI assistive bot that helps with automating your daily tasks as it communicates with your voice as input and your desktop. 

## ROS2 inspired - System Architecture Flow 
How I imagined the flow and interaction between the different systems, my logic to use two separate languages python and C++ was to simulate and leverage the advantages of both. 
I wanted a modular design, ROS2 based workflows work for bots so that many different systems, programs and actions can occur after it gather's its' input, having a communication/logic layer between that to decide what function to perform and ensures better debugging ability. 

## How to Setup 

## Reflection/learning outcomes 
- Implementing C++ was a design-decision choice to allow efficient decision making when it came to add more gestures. Since this is modular design, this makes it way faster when upgrading and doing further improvements/features
