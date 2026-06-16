from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool

import os

search_tool = SerperDevTool()
@CrewBase
class BasicCrewai():
    """BasicCrewai crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def investigator(self) -> Agent:
        return Agent(
            config=self.agents_config['investigator'], # type: ignore[index]
            verbose=True,
            tools = [search_tool],
            llm = LLM(model=os.environ.get("OPENAI_MODEL_NAME"),
                      api_key=os.environ.get("OPENAI_API_KEY"),
                      base_url=os.environ.get("OPENAI_BASE_URL"),
            )
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def copywriter(self) -> Agent:
        return Agent(
            config=self.agents_config['copywriter'], # type: ignore[index]
            verbose=True,
            llm = LLM(model=os.environ.get("ANTHROPIC_MODEL_NAME"),
                      api_key=os.environ.get("OPENAI_API_KEY"),
                      base_url=os.environ.get("OPENAI_BASE_URL"),
            )
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'], # type: ignore[index]
            output_file='report.md'
        )
    @task
    def email_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_task'], # type: ignore[index]
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BasicCrewai crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
