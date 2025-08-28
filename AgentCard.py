# host_agent.py
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
from google.adk.tools import AgentTool

# Remote agents
jira_tool = AgentTool.from_url("http://jira-agent-server/agent.json")
content_tool = AgentTool.from_url("http://content-author-server/agent.json")
task_tool = AgentTool.from_url("http://task-agent-server/agent.json")

# ---- Stage 1: Jira Description ----
jira_desc_agent = LlmAgent(
    name="JiraDescriptionFetcher",
    model="gemini-1.5-pro",
    tools=[jira_tool],
    instruction="""
    - Ensure a Jira ID (PROJECT-123) exists.
    - If missing, ask: "Please provide a Jira ID."
    - Once Jira ID available, call JiraAgent.get_description(jira_id).
    - Save result to {jira_description}.
    """,
    output_key="jira_description"
)

# ---- Stage 2: Jira Attachments ----
jira_attachment_agent = LlmAgent(
    name="JiraAttachmentFetcher",
    model="gemini-1.5-pro",
    tools=[jira_tool],
    instruction="""
    Jira description:
    {jira_description}

    - Identify FRD and Message Spec attachment names.
    - For each, call JiraAgent.get_attachment(jira_id, attachment_name).
    - Save as structured JSON:
      {
        "FRD": { "attachment_name": "FRD.docx", "content": "<content>" },
        "MessageSpec": { "attachment_name": "MessageSpec.xlsx", "content": "<content>" }
      }
    - Store in {jira_attachments}.
    """,
    output_key="jira_attachments"
)

# ---- Stage 3a: Content Author Agent ----
content_author_agent = LlmAgent(
    name="ContentAuthorWrapper",
    model="gemini-1.5-pro",
    tools=[content_tool],
    instruction="""
    From Jira attachments:
    {jira_attachments}

    - Extract FRD: jira_id + attachment_name + content
    - Call ContentAuthorAgent with:
      {
        "jira_id": "<id>",
        "attachment_name": "<FRD name>",
        "attachment_content": "<FRD content>"
      }
    """,
    output_key="authored_content"
)

# ---- Stage 3b: Task Agent ----
task_agent = LlmAgent(
    name="TaskWrapper",
    model="gemini-1.5-pro",
    tools=[task_tool],
    instruction="""
    From Jira attachments:
    {jira_attachments}

    - Extract Message Spec: jira_id + attachment_name + content
    - Call TaskAgent with:
      {
        "jira_id": "<id>",
        "attachment_name": "<MsgSpec name>",
        "attachment_content": "<MsgSpec content>"
      }
    """,
    output_key="tasks_created"
)

# ---- Stage 3: Parallel Execution ----
parallel_stage = ParallelAgent(
    name="ParallelStage",
    sub_agents=[content_author_agent, task_agent],
    description="Runs Content Author + Task Agent in parallel"
)

# ---- Final Host Workflow ----
root_agent = SequentialAgent(
    name="HostWorkflowAgent",
    sub_agents=[jira_desc_agent, jira_attachment_agent, parallel_stage],
    description="Host Agent: Jira → Attachments → (Content Author + Task)"
)
