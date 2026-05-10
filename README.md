# AI Marketing Agent: Notion to Canva Pipeline

### The Vision
As a technical marketer, I noticed a gap between content strategy and asset creation. This project is an autonomous AI agent that bridges that gap. It reads marketing strategies directly from **Notion** databases and automatically generates brand-aligned social media assets via the **Canva API**.

### Architecture & "Vibe"
Rather than hardcoding manual scripts, this agent is built on **LangGraph** and utilizes the **Model Context Protocol (MCP)**. This allows the AI to dynamically call tools only when conversational intent demands it. 
* **Brain:** Google Gemini 2.5 Flash via LangChain.
* **Knowledge Base:** Notion MCP (fetches dates, copy, and campaign strategies).
* **Design Engine:** Canva MCP (applies the "Ikenna" brand kit and exports high-res imagery).

### How it Works
1. **Intent Recognition:** The agent chats with the user to brainstorm. 
2. **Context Retrieval:** Once a date is decided, it queries Notion for that day's specific marketing goals.
3. **Asset Generation:** It passes the Notion data and strict brand guidelines into Canva.
4. **Delivery:** It outputs a direct, downloadable URL for the finished marketing flyer.
