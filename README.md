CSE Course Recommendation

Abstract: 
The Computer Science and Engineering Department at UC Merced has been committed to optimizing educational pathways for its students, specifically in aligning course selections with their academic prerequisites and career ambitions. The existing tool, My Degree Path, although effective for general academic planning, has limitations in accommodating the specialized needs of Computer Science and Engineering students, particularly in selecting CSE electives that match their career trajectories. The team has leveraged the OpenAI API to develop a system that utilizes ChatGPT to interact directly with students. This system understands students' career interests and integrates this data with their academic prerequisites and UC Merced’s available courses. By providing personalized educational guidance tailored to individual career goals, this approach ensures a more aligned and effective educational journey for each student.

Instructions:
Setting up	- 
1. Open your chosen terminal/IDE.
2. Enter the following command to clone the project repository and acquire a local copy of the project.
      git clone https://github.com/jenvrosen/capstoneProject.git
3. Navigate to the root folder of the project directory.
      cd capstoneProject
4. Create a virtual environment.
      python -m venv venv	(For windows)
      python3 -m venv venv	(For macOS)
5. Activate your created virtual environment.
      .\venv\Scripts\activate	(For windows)
      source venv/bin/activate	(For macOS)
6. Install the required dependencies.
      pip install -r requirements.txt
7. Run the application.
      python run.py
8. Open a web browser and enter ‘http://localhost:5000’.
