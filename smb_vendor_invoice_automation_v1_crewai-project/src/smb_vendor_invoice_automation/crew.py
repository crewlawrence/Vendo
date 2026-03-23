import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	OCRTool
)





@CrewBase
class SmbVendorInvoiceAutomationCrew:
    """SmbVendorInvoiceAutomation crew"""

    
    @agent
    def vendor_invoice_processor(self) -> Agent:
        
        return Agent(
            config=self.agents_config["vendor_invoice_processor"],
            
            
            tools=[				OCRTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            apps=[
                    "google_gmail/fetch_emails",
                    
                    "google_gmail/get_message",
                    
                    "google_gmail/get_attachment",
                    ],
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
                
            ),
            
        )
    
    @agent
    def invoice_data_organizer(self) -> Agent:
        
        return Agent(
            config=self.agents_config["invoice_data_organizer"],
            
            
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            apps=[
                    "google_sheets/append_values",
                    
                    "google_sheets/create_spreadsheet",
                    ],
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
                
            ),
            
        )
    

    
    @task
    def monitor_and_extract_vendor_invoices(self) -> Task:
        return Task(
            config=self.tasks_config["monitor_and_extract_vendor_invoices"],
            markdown=False,
            
            
        )
    
    @task
    def organize_invoice_data_for_quickbooks(self) -> Task:
        return Task(
            config=self.tasks_config["organize_invoice_data_for_quickbooks"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the SmbVendorInvoiceAutomation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )


