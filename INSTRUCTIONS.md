# Assignment: Docker Setup and LLM-Assisted TODO Implementation

**Overview**  
This assignment develops your skills in container-based development, LLM-assisted implementation, Git branching workflows, and validation using Docker Desktop and GitHub Copilot Agents. You will run the project inside a container and complete three TODO items, each in its own branch of your fork. All TODO items must be fully implemented, tested, and validated.

---

## Part 1: Install Docker and Build the Existing Container

The repository includes:

- A complete **Dockerfile**
- A complete **docker compose YAML file**
- **Docker installation and usage instructions**

Your tasks:

1. **Fork** the repository (done when starting the GitHub Classroom assignment).  
2. Install Docker following the instructions in the repo.  
3. Build the Docker image using the existing Dockerfile.  
4. Run the container using Docker Compose or the appropriate Docker commands.  
5. Confirm that the application starts and runs correctly.

Your short write-up should confirm:

- Docker installed correctly  
- The image built successfully  
- The container ran without errors  

---

## Part 2: Complete Three TODO Items (Each in Its Own Branch, With Tests)

Open [docs/TODO.md](docs/TODO.md) in the repository. Each item includes a severity level.

### Requirements

1. Choose **three** TODO items.  
2. **At least two** must have **medium or high severity**.  
3. For each TODO item:
   - Create a **separate branch** in your fork:
     ```
     todo-<short-description>
     ```
     Example: `todo-audio-normalization`
   - Use an LLM to assist in producing a complete and correct implementation.  
   - Use the LLM to write **tests** for the TODO, following the style and structure of the existing tests in the repo.
   - Build and run the project **inside the Docker container** to validate your work.  
   - Refine implementation and tests until everything passes.  
   - Keep each TODO and its tests self-contained within its branch.
   - If using a chat-based LLM:
     - Maintain an `AGENT-TRANSCRIPT-<todo-title>.md` file with a summary of the LLM conversation.
     - Push each branch to `origin`
     - Create a Pull Request to merge the branch into main
   - Othewise, for Agent Tasks in Github, the Branch and Pull Requests are already created by the Agent.

### GitHub Copilot Agent Requirement

On **at least one** of your TODO branches:

- Push the branch to your fork, if not already done.
- Create a **GitHub Copilot Agent Task** to review your implementation and tests.  
  (If Copilot Agent was used throughout from the start, the review task is optional but recommended.)
- Include evidence of the Copilot review in your submission by leaving the branch and Pull Request in the repository.

---

## Part 3: Submit Evidence of Your Work

Your submission must include:

### 1. A write-up in the file named [PA4-README.md](PA4-README.md)
Include:

- Minimal documentation as given in the syllabus
- Links to your **three TODO branches**  and all **Pull Requests** created
- Prompts used for:
  - Implementations  
  - Test generation  
  - Copilot Agent review (where applicable)<br>
    Note: These can be provided in the relevant transcripts but links must be provided in the `PA4-README.md`
- Reflection: Short explanations of accepted vs. rejected LLM suggestions  
- Confirmation that the implementation and tests run successfully inside Docker  

### 2. Evidence of Docker Execution

Include **screenshots** of Docker Desktop (or equivalent Docker environment) showing:

- The built image  
- The running container  
- That the container is healthy / functioning

These screenshots can be provided as separate image files.

### 3. Copilot Agent Review Evidence

For the branch reviewed by Copilot:

- Include:
  - Copilot Agent task output, OR  
  - A screenshot of the task results, OR  
  - A brief summary if Copilot was used continuously from the start  

---

## Completion Requirements

To receive full credit, you must:

- Install Docker successfully  
- Build and run the container  
- Fork the repo and create **three separate TODO branches**  
- Fully implement three TODO items  
- Ensure **two TODO items** are medium/high severity  
- Generate and validate tests for each TODO  
- Confirm everything runs inside Docker  
- Use GitHub Copilot Agent review on at least one branch  
- Provide Docker Desktop screenshots showing container execution  
- Provide diff PDFs for each branch  
- Provide a write-up documenting LLM usage and decisions  

