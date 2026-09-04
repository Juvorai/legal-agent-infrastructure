---
name: server-discovery
description: Reference for all server types, connected integrations, and available servers.
---

# Server Discovery

Tool slugs use `server_id__tool_name` (double underscore). Use `tool_discovery` to get exact slugs.

The catalog below is long — a full read of this file may truncate before the entry you need.
To check whether a specific service exists, use sandbox_python to search this file for the service name.
Never conclude a service is absent from a truncated read.

## Adding a Server

Use `add_server_awaiter` with the `server_id` to add any server to this agent. Identify ALL servers a task needs upfront and add them in a single step (parallel tool calls).

## All Servers

| server_id | name | type | capability | status | authenticated | description |
|-----------|------|------|------------|--------|---------------|-------------|
| affinity | affinity | gumcp_server | manage_records | available | no | Get all opportunities in list "Prospects" |
| ahrefs | ahrefs | gumcp_server | get_data | available | no | Get backlink data for a domain and list referring domains with DR > 50 |
| airtable | airtable | gumcp_server | get_data | connected | yes | List all records in the "Leads" table created this month |
| apify | apify | gumcp_server | scrape_web | available | n/a | Run an Apify actor to extract product data from an e-commerce site |
| apollo | apollo | gumcp_server | enrich_data | connected | n/a | Enrich a contact by email |
| applovin | applovin | gumcp_server | get_data | available | no | Get a report of my AppLovin campaign performance for the last 7 days |
| asana | asana | gumcp_server | manage_tasks | available | no | Get all tasks in a project |
| ashby | ashby | gumcp_server | recruiting | available | no | Get all candidates in the last month |
| attio | attio | gumcp_server | manage_records | available | no | Get contact details for john.doe@email.com and show recent interactions |
| azure_cloud | azure_cloud | gumcp_server | automation | available | no | List all resource groups in my subscription |
| beehiiv | beehiiv | gumcp_server | bulk_email | available | no | Add a subscriber to my newsletter using their email |
| bing_webmaster | bing_webmaster | gumcp_server | get_data | available | no | Show the top search queries and clicks for my site this month |
| box | box | gumcp_server | manage_files | available | no | List files in my root folder |
| brandfetch | brandfetch | gumcp_server | enrich_data | available | n/a | Look up brand data, logos, and colors for gumloop.com |
| cal | cal | gumcp_server | schedule | available | no | List all events in my calendar for the next 3 days with location details |
| chorus | chorus | gumcp_server | get_data | available | no | Search meetings or calls |
| clickhouse | clickhouse | gumcp_server | get_data | available | no | Query a ClickHouse Cloud service or manage dashboards and alerts |
| clickup | clickup | gumcp_server | manage_tasks | available | no | List all tasks in the "Marketing" space due this week |
| confluence | confluence | gumcp_server | create_content | available | no | List all pages in a specific space |
| cursor | cursor | gumcp_server | automation | available | no | Launch a Cursor agent to implement a feature |
| databricks | databricks | gumcp_server | get_data | available | no | Query the serving endpoint |
| datadog | datadog | gumcp_server | get_data | available | no | List all monitors in critical state |
| dataforseo | dataforseo | gumcp_server | get_data | available | n/a | Find the keywords a competitor ranks for |
| devin | devin | gumcp_server | automation | available | no | Create a Devin session to fix a bug |
| docusign | docusign | gumcp_server | manage_records | connected | yes | List all envelopes from the last 30 days |
| exa | exa | gumcp_server | search_web | connected | n/a | Search the web with AI |
| excel | excel | gumcp_server | get_data | available | no | Get all rows from the "Q2 Sales" sheet where status is "Closed Won" |
| expensify | expensify | gumcp_server | payments | available | no | Get all transactions in the last month |
| extend | extend | gumcp_server | automation | available | no | Process files or documents through workflows |
| fal | fal | gumcp_server | create_content | available | n/a | Generate an image of a sunset over mountains |
| fathom | fathom | gumcp_server | get_data | available | no | Get the transcript and summary from my last meeting |
| fellow | fellow | gumcp_server | get_data | available | no | Access meeting recordings, notes, and transcripts |
| findymail | findymail | gumcp_server | enrich_data | available | no | Find verified email addresses and phone numbers for contacts |
| firecrawl | firecrawl | gumcp_server | scrape_web | connected | n/a | Search, scrape, crawl, or map websites for data with Firecrawl |
| foreplay | foreplay | gumcp_server | get_data | available | n/a | Get all brands |
| freshdesk | freshdesk | gumcp_server | support | available | no | List all open tickets from the last week |
| freshsales | freshsales | gumcp_server | manage_records | available | no | List contacts and deals in Freshsales |
| gads | gads | gumcp_server | get_data | available | no | Get all campaigns for a specific account |
| gamma | gamma | gumcp_server | create_content | available | no | Create a new presentation |
| ganalytics | ganalytics | gumcp_server | get_data | available | no | Get website traffic for the last 7 days broken down by country |
| gappsheet | gappsheet | gumcp_server | get_data | available | no | Get all rows from a table where status is "Active" |
| gappsscript | gappsscript | gumcp_server | automation | available | no | Create a new script |
| gbigquery | gbigquery | gumcp_server | get_data | available | no | Run a SQL query on a dataset to get total sales for Q1 2024 |
| gcalendar | gcalendar | gumcp_server | schedule | available | yes | Give me all meetings from the previous 24 hours with more than 2 attendees |
| gcs | gcs | gumcp_server | manage_files | available | no | Manage files and buckets |
| gdocs | gdocs | gumcp_server | create_content | available | no | Find all documents shared with me by Alice in the last month |
| gdrive | gdrive | gumcp_server | manage_files | connected | yes | Get all files in a folder that have "budget" in the file name |
| gdv360 | gdv360 | gumcp_server | get_data | available | no | Get all campaigns for a specific account |
| github | github | gumcp_server | manage_tasks | connected | yes | List all repositories for a user and show the number of open issues for each |
| gitlab | gitlab | gumcp_server | manage_tasks | available | no | Open a merge request from feature/x into main on mygroup/myproject |
| glooker | glooker | gumcp_server | get_data | available | no | Interact with Google Looker to run queries, manage dashboards, and schedule deliveries |
| gmail | gmail | gumcp_server | send_message | available | yes | Retrieve the last 5 unread emails with attachments from my inbox |
| gmaps | gmaps | gumcp_server | get_data | available | n/a | Get directions from my current location to the office |
| gmeet | gmeet | gumcp_server | schedule | available | no | Create a new meeting for the "Engineering" team tomorrow at 10am |
| gnotebooklm | gnotebooklm | gumcp_server | create_content | available | no | Create a NotebookLM notebook, add sources, and generate an audio overview |
| gong | gong | gumcp_server | get_data | available | no | List all calls in the last 30 days |
| gpagespeed | gpagespeed | gumcp_server | get_data | available | n/a | Analyze the performance of a website |
| greenhouse | greenhouse | gumcp_server | recruiting | available | no | Get all candidates in the last month |
| gsearchconsole | gsearchconsole | gumcp_server | get_data | available | no | Show me top search queries for my site over the last 30 days |
| gsheets | gsheets | gumcp_server | get_data | available | no | Get all rows from the "Q2 Sales" sheet where status is "Closed Won" |
| gslides | gslides | gumcp_server | create_content | available | no | Create a presentation about Q1 results with charts and speaker notes |
| gtasks | gtasks | gumcp_server | manage_tasks | available | no | Manage tasks and task lists |
| hex | hex | gumcp_server | get_data | available | no | List all projects in my Hex workspace |
| hubspot | hubspot | gumcp_server | manage_records | available | no | Find a contact by email and show their last 3 deals |
| incident_io | incident_io | gumcp_server | support | available | no | Create a critical incident for database outage |
| instagram | instagram | gumcp_server | social_media | available | n/a | Get comments on a post |
| intercom | intercom | gumcp_server | manage_records | available | no | Get all users in the last month |
| jira | jira | gumcp_server | manage_tasks | available | no | List all issues assigned to me in the "Backend" project with priority High |
| launchdarkly | launchdarkly | gumcp_server | get_data | available | no | List all feature flags in a project |
| linear | linear | gumcp_server | manage_tasks | available | no | List all open issues assigned to me in the "Website Redesign" project |
| loops | loops | gumcp_server | bulk_email | available | no | Create a new contact |
| luma | luma | gumcp_server | schedule | available | no | List all upcoming events on my Luma calendar |
| meta_ads | meta_ads | gumcp_server | get_data | available | no | Show spend for my campaigns last 30 days |
| monday | monday | gumcp_server | manage_tasks | connected | yes | List all items in the "Product Launch" board with status "In Progress" |
| netsuite | netsuite | gumcp_server | manage_records | available | no | Get all customers in the last month |
| notion | notion | gumcp_server | create_content | available | no | Find a page by title and list all subpages created in 2024 |
| outlook | outlook | gumcp_server | send_message | available | no | Get my last 10 unread emails |
| outlook_calendar | outlook_calendar | gumcp_server | schedule | available | no | Get all my meetings for today |
| outreach | outreach | gumcp_server | manage_records | available | no | Add the new prospects from this list to the "Q3 Enterprise" sequence |
| pagerduty | pagerduty | gumcp_server | support | available | no | Get all alerts in the last 24 hours |
| parallel | parallel | gumcp_server | search_web | available | n/a | Search the web with AI |
| pipedrive | pipedrive | gumcp_server | manage_records | available | no | Get all deals in the last month |
| postgresql | postgresql | gumcp_server | get_data | available | no | Get all tables in a database |
| quickbooks | quickbooks | gumcp_server | payments | available | no | Analyze cash flow trends and generate financial metrics for my business |
| rads | rads | gumcp_server | get_data | available | no | List all campaigns in my Reddit ad account and their status |
| reddit | reddit | gumcp_server | social_media | available | no | Get the latest posts from the r/machinelearning subreddit with more than 100 upvotes |
| reducto | reducto | gumcp_server | other | available | n/a | Summarize a document and highlight the top 3 key points |
| salesforce | salesforce | gumcp_server | manage_records | available | no | Get Account details by account id and list all open opportunities |
| salesloft | salesloft | gumcp_server | manage_records | available | no | Get all contacts in the last month |
| seismic | seismic | gumcp_server | get_data | available | no | Perform operations on Seismic content, users, and engagements |
| semrush | semrush | gumcp_server | get_data | available | no | Get all keywords for a specific domain |
| sharepoint | sharepoint | gumcp_server | manage_files | available | no | Find the Marketing site and list its document libraries |
| shopify | shopify | gumcp_server | payments | available | no | List all products in the store that are out of stock |
| sigma_computing | sigma_computing | gumcp_server | get_data | available | no | Interact with Sigma Computing to manage workbooks, data, and analytics |
| slack | slack | gumcp_server | send_message | available | yes | Get all messages from the #general channel from Ben in the last 3 days |
| snapchat_ads | snapchat_ads | gumcp_server | get_data | available | no | Show impressions and spend for my Snapchat campaigns |
| snowflake | snowflake | gumcp_server | get_data | available | no | Get all tables in a database |
| sprig | sprig | gumcp_server | get_data | available | no | Retrieve survey responses and analyze user feedback |
| sprout_social | sprout_social | gumcp_server | social_media | available | no | Pull profile analytics or schedule a draft post in Sprout Social |
| stripe | stripe | gumcp_server | payments | available | no | Get all invoices for a specific customer |
| tableau | tableau | gumcp_server | get_data | available | no | Interact with Tableau to access dashboards, data, and metrics |
| teams | teams | gumcp_server | send_message | available | no | Get all members in a team |
| tiktok | tiktok | gumcp_server | social_media | available | n/a | Get comments on a post |
| trello | trello | gumcp_server | manage_tasks | available | no | List all cards on my "Product Roadmap" board |
| webflow | webflow | gumcp_server | create_content | available | no | List all sites and collections |
| word | word | gumcp_server | create_content | available | no | Create a document with the title "AI Trends 2050" |
| workday | workday | gumcp_server | recruiting | available | no | Download report from url |
| x | x | gumcp_server | social_media | available | no | Search for tweets about AI and get the top 10 results |
| youtube | youtube | gumcp_server | social_media | available | n/a | Get all videos from a channel |
| zendesk | zendesk | gumcp_server | support | available | no | List all open tickets assigned to the "Support" group in the last 48 hours |
| zoom | zoom | gumcp_server | schedule | available | no | Get all meetings in the last month |
| 9dlepf9x92v6ahkxtpqka8 | App | gumstack_server | - | connected | yes | App |
| gzzdsahbntihvm4nntgkfa | Midpage | gumstack_server | - | connected | yes | Midpage |
| jeczhy8zbaynf3uvgaskwm | Patent Connector | gumstack_server | - | connected | yes | Patent Connector |
| carta | Carta | gumstack_server | - | connected | yes | Carta |
| todoist | Todoist | gumstack_server | - | connected | yes | Todoist |
| midpage-legal-research | Midpage | gumstack_server | - | connected | yes | Midpage |
| browserbase | Browserbase | gumstack_server | - | connected | yes | Browserbase |
| agentmail | AgentMail | gumstack_server | - | connected | yes | AgentMail |
| actively | Actively | gumstack_server | - | available | no | Access Actively account intelligence, signals, and recommended sales actions. |
| adisinsight | AdisInsight | gumstack_server | - | available | no | Search AdisInsight drug development, clinical trial, and pipeline intelligence. |
| adobe-marketing-agent | Adobe Marketing Agent | gumstack_server | - | available | no | Analyze and act on your Adobe Experience Platform marketing data. |
| airops | AirOps | gumstack_server | - | available | no | Build and run AirOps AI content and marketing workflows. |
| airwallex-developer | Airwallex | gumstack_server | - | available | no | Manage your Airwallex payments, accounts, and financial operations. |
| alma | Alma | gumstack_server | - | available | no | Track your nutrition and meals with your Alma AI coach. |
| alpic | Alpic | gumstack_server | - | available | no | Deploy and monitor your MCP servers and apps on Alpic. |
| attention | Attention | gumstack_server | - | available | no | Access Attention call insights, coaching, and CRM updates. |
| aura | Aura | gumstack_server | - | available | no | Analyze workforce trends, hiring, and competitor benchmarks with Aura. |
| aurora | Aurora | gumstack_server | - | available | no | Search your Consilio matters, workspaces, documents, and tickets. |
| basedash | Basedash | gumstack_server | - | available | no | Create and manage Basedash charts, dashboards, and database insights. |
| biorender | BioRender | gumstack_server | - | available | no | Create and manage scientific figures and illustrations in BioRender. |
| biomni-lab | Biomni Lab | gumstack_server | - | available | no | Run biomedical research and bioinformatics tasks with Biomni. |
| bitly | Bitly | gumstack_server | - | available | no | Create Bitly short links and track their click analytics. |
| brevo | Brevo | gumstack_server | - | available | no | Manage your Brevo email campaigns, contacts, and marketing automation. |
| brisk-teaching | Brisk Teaching | gumstack_server | - | available | no | Create teaching materials, feedback, and lessons with Brisk Teaching. |
| cb-insights | CB Insights | gumstack_server | - | available | no | Research companies, markets, and funding trends with CB Insights. |
| cdata-connect-ai | CData Connect AI | gumstack_server | - | available | no | Connect to your databases and SaaS data sources through CData Connect. |
| caffeine | Caffeine | gumstack_server | - | available | no | Build and manage web apps with Caffeine's AI app builder. |
| campfire | Campfire | gumstack_server | - | available | no | Manage your Campfire accounting, ledger, and financial workflows. |
| candid | Candid | gumstack_server | - | available | no | Access Candid nonprofit, grant, and foundation data. |
| canva | Canva | gumstack_server | - | available | no | Design and manage Canva assets, designs, and brand content. |
| cargoai | CargoAi | gumstack_server | - | available | no | Search air cargo capacity, rates, and bookings with CargoAi. |
| chronograph | Chronograph | gumstack_server | - | available | no | Access Chronograph private equity portfolio and fund data. |
| circleback | Circleback | gumstack_server | - | available | no | Search and access your Circleback meeting notes and action items. |
| clarify | Clarify | gumstack_server | - | available | no | Manage your Clarify CRM contacts, deals, and records. |
| clay | Clay | gumstack_server | - | available | no | Enrich leads and run go-to-market data workflows with Clay. |
| close | Close | gumstack_server | - | available | no | Manage your Close CRM leads, contacts, and opportunities. |
| cloudflare | Cloudflare | gumstack_server | - | available | no | Manage your Cloudflare account, DNS, and Workers. |
| cloudinary | Cloudinary | gumstack_server | - | available | no | Manage and transform your Cloudinary images and media assets. |
| coindesk | CoinDesk | gumstack_server | - | available | no | Access CoinDesk cryptocurrency market data and news. |
| common-room | Common Room | gumstack_server | - | available | no | Track customer and community signals with Common Room. |
| contentsquare | Contentsquare | gumstack_server | - | available | no | Analyze digital experience and web behavior data with Contentsquare. |
| context7 | Context7 | gumstack_server | - | available | n/a | Fetch up-to-date library documentation and code examples with Context7. |
| cortellis-regulatory-intelligence | Cortellis Regulatory Intelligence | gumstack_server | - | available | no | Search Cortellis drug regulatory intelligence and filings. |
| courtlistener | CourtListener | gumstack_server | - | available | no | Search U.S. court opinions, dockets, and case law on CourtListener. |
| craft | Craft | gumstack_server | - | available | no | Create and manage your Craft documents and notes. |
| crossbeam | Crossbeam | gumstack_server | - | available | no | Map partner accounts and overlaps with Crossbeam. |
| daloopa | Daloopa | gumstack_server | - | available | no | Pull source-linked financial fundamentals and KPIs with Daloopa. |
| datahub | DataHub | gumstack_server | - | available | no | Search your data catalog, lineage, and metadata in DataHub. |
| day-ai | Day AI | gumstack_server | - | available | no | Manage your Day AI CRM relationships and customer context. |
| definely | Definely | gumstack_server | - | available | no | Draft and review complex contracts with Definely. |
| demographic-and-health-surveys | Demographic and Health Surveys | gumstack_server | - | available | no | Access Demographic and Health Surveys population and health data. |
| descript | Descript | gumstack_server | - | available | no | Edit and manage your Descript audio and video projects. |
| descrybe-legal-engine | Descrybe Legal Engine | gumstack_server | - | available | no | Search and summarize case law with Descrybe's legal engine. |
| digits | Digits | gumstack_server | - | available | no | Access your Digits accounting, financials, and reports. |
| eden-by-basecamp-research | EDEN by Basecamp Research | gumstack_server | - | available | no | Explore biological sequence and evolutionary data with Basecamp Research's EDEN. |
| egnyte | Egnyte | gumstack_server | - | available | no | Access and manage your Egnyte files and content. |
| elevenlabs | ElevenLabs | gumstack_server | - | available | no | Generate speech, voices, and audio with ElevenLabs. |
| elicit | Elicit | gumstack_server | - | available | no | Search and synthesize research papers with Elicit. |
| embat | Embat | gumstack_server | - | available | no | Manage treasury, cash flow, and finances with Embat. |
| enterpret | Enterpret | gumstack_server | - | available | no | Analyze customer feedback and product insights with Enterpret. |
| entropia | Entropia | gumstack_server | - | available | no | Manage your Entropia data room documents and due diligence. |
| era-context | Era Context | gumstack_server | - | available | no | Access your accounts, transactions, and financial context with Era. |
| eraser | Eraser | gumstack_server | - | available | no | Create diagrams and technical design docs with Eraser. |
| euler | Euler | gumstack_server | - | available | no | Manage your partner programs, deals, and referrals with Euler. |
| factset-ai-ready-data | FactSet | gumstack_server | - | available | no | Access FactSet financial market and company data. |
| felt-maps | Felt | gumstack_server | - | available | no | Create and manage collaborative maps in Felt. |
| fever-event-discovery | Fever | gumstack_server | - | available | no | Discover local events and experiences with Fever. |
| fireflies | Fireflies | gumstack_server | - | available | no | Search and access your Fireflies meeting transcripts and notes. |
| fiscal-ai | Fiscal.ai | gumstack_server | - | available | no | Access company financials, KPIs, and market data with Fiscal.ai. |
| gainsight | Gainsight | gumstack_server | - | available | no | Access Gainsight customer success health, accounts, and signals. |
| gocardless | GoCardless | gumstack_server | - | available | no | Manage GoCardless payments, mandates, and payouts. |
| grain | Grain | gumstack_server | - | available | no | Search and access your Grain meeting recordings and notes. |
| granola | Granola | gumstack_server | - | available | no | Search and access your Granola meeting notes. |
| guru | Guru | gumstack_server | - | available | no | Search your company knowledge and cards in Guru. |
| gusto | Gusto | gumstack_server | - | available | no | Manage your Gusto payroll, employees, and benefits. |
| harmonic | Harmonic | gumstack_server | - | available | no | Research startups and private company data with Harmonic. |
| honeycomb | Honeycomb | gumstack_server | - | available | no | Query your Honeycomb observability data, traces, and events. |
| hugging-face | Hugging Face | gumstack_server | - | available | no | Explore Hugging Face models, datasets, and Spaces. |
| hyperframes-by-heygen | HyperFrames by HeyGen | gumstack_server | - | available | no | Generate AI images and video frames with HeyGen HyperFrames. |
| ibisworld | IBISWorld | gumstack_server | - | available | no | Access IBISWorld industry research and market reports. |
| inductive-bio | Inductive Bio | gumstack_server | - | available | no | Support small-molecule drug discovery and modeling with Inductive Bio. |
| jam | Jam | gumstack_server | - | available | no | Access your Jam bug reports and debug logs. |
| jentic | Jentic | gumstack_server | - | available | no | Discover and execute APIs and workflows for your agents with Jentic. |
| jotform | Jotform | gumstack_server | - | available | no | Create and manage your Jotform forms and submissions. |
| ketryx | Ketryx | gumstack_server | - | available | no | Manage regulated software compliance and lifecycle with Ketryx. |
| klarity | Klarity | gumstack_server | - | available | no | Map and document business processes with Klarity. |
| klaviyo | Klaviyo | gumstack_server | - | available | no | Manage Klaviyo profiles, campaigns, lists, and marketing data. |
| kpler | Kpler | gumstack_server | - | available | no | Access Kpler commodity, shipping, and trade flow data. |
| krea | Krea | gumstack_server | - | available | no | Generate images and video, enhance and upscale assets with Krea. |
| krisp | Krisp | gumstack_server | - | available | no | Access your Krisp meeting notes, transcripts, and summaries. |
| lilt | LILT | gumstack_server | - | available | no | Manage translation and localization projects with LILT. |
| latchbio | LatchBio | gumstack_server | - | available | no | Run bioinformatics workflows and manage biological data with LatchBio. |
| lawve-ai | Lawve AI | gumstack_server | - | available | no | Discover expert-written legal skills and workflows with Lawve AI. |
| legal-data-hunter | Legal Data Hunter | gumstack_server | - | available | no | Search case law, legislation, and legal sources worldwide with Legal Data Hunter. |
| lightfield | Lightfield | gumstack_server | - | available | no | Manage your Lightfield CRM accounts, contacts, and conversations. |
| listen-labs | Listen Labs | gumstack_server | - | available | no | Run and analyze AI-moderated user research with Listen Labs. |
| local-falcon | Local Falcon | gumstack_server | - | available | no | Track local search rankings and Google Business visibility with Local Falcon. |
| lucid | Lucid | gumstack_server | - | available | no | Create and manage Lucid diagrams and visual workspaces. |
| lumin | Lumin | gumstack_server | - | available | no | Edit, sign, and manage your PDFs with Lumin. |
| lumonic | Lumonic | gumstack_server | - | available | no | Manage private credit portfolios and loan data with Lumonic. |
| lunarcrush | LunarCrush | gumstack_server | - | available | no | Track crypto and social market sentiment with LunarCrush. |
| mt-newswires | MT Newswires | gumstack_server | - | available | no | Access MT Newswires financial and market news. |
| magic-patterns | Magic Patterns | gumstack_server | - | available | no | Generate and iterate on UI designs and prototypes with Magic Patterns. |
| mailerlite | MailerLite | gumstack_server | - | available | no | Manage your MailerLite subscribers, campaigns, and automations. |
| make | Make | gumstack_server | - | available | no | Trigger and manage your Make automation scenarios. |
| manufact | Manufact | gumstack_server | - | available | no | Deploy and manage your MCP servers and apps with Manufact. |
| medidata | Medidata | gumstack_server | - | available | no | Access Medidata clinical trial data and study operations. |
| mem | Mem | gumstack_server | - | available | no | Search and manage your Mem notes and knowledge. |
| mercury | Mercury | gumstack_server | - | available | no | Manage your Mercury business banking, transactions, and payments. |
| metaview | Metaview | gumstack_server | - | available | no | Access your Metaview interview notes and hiring insights. |
| microsoft-learn | Microsoft Learn | gumstack_server | - | available | n/a | Search Microsoft Learn documentation and code samples. |
| mintlify | Mintlify | gumstack_server | - | available | no | Edit your Mintlify docs, navigation, and settings. |
| miro | Miro | gumstack_server | - | available | no | Create and manage your Miro boards and content. |
| mixpanel | Mixpanel | gumstack_server | - | available | no | Query your Mixpanel product analytics and user events. |
| monte-carlo | Monte Carlo | gumstack_server | - | available | no | Monitor data quality and pipeline health with Monte Carlo. |
| morningstar | Morningstar | gumstack_server | - | available | no | Access Morningstar investment research and market data. |
| motherduck | MotherDuck | gumstack_server | - | available | no | Query your MotherDuck data warehouse and run analytics. |
| motion-creative-analytics | Motion Creative Analytics | gumstack_server | - | available | no | Analyze ad creative performance with Motion. |
| netlify | Netlify | gumstack_server | - | available | no | Manage your Netlify sites, deploys, and configuration. |
| o-reilly | O'Reilly | gumstack_server | - | available | no | Search O'Reilly books, courses, and learning content. |
| omni-analytics | Omni | gumstack_server | - | available | no | Explore and query your data with Omni analytics. |
| ontra | Ontra | gumstack_server | - | available | no | Manage legal contracts and obligations with Ontra. |
| origin | Origin | gumstack_server | - | available | no | Monitor AI agents, actions, and endpoint activity with Origin. |
| orion-by-gravity | Orion by Gravity | gumstack_server | - | available | no | Run autonomous data analyses and insights with Orion by Gravity. |
| otter-ai | Otter.ai | gumstack_server | - | available | no | Search and access your Otter meeting notes and transcripts. |
| otto-travel | Otto Travel | gumstack_server | - | available | no | Plan and book business travel with your Otto AI assistant. |
| pandadoc | PandaDoc | gumstack_server | - | available | no | Create, send, and track PandaDoc documents and e-signatures. |
| paypal | PayPal | gumstack_server | - | available | no | Manage your PayPal payments, invoices, and transactions. |
| peec-ai | Peec AI | gumstack_server | - | available | no | Track your brand visibility across AI search engines with Peec AI. |
| phoenix-by-hg-insights | Phoenix by HG Insights | gumstack_server | - | available | no | Access HG Insights technographic and market intelligence data. |
| planetscale | PlanetScale | gumstack_server | - | available | no | Manage your PlanetScale databases, branches, and schemas. |
| polar-analytics | Polar Analytics | gumstack_server | - | available | no | Analyze your ecommerce and marketing metrics with Polar Analytics. |
| postman | Postman | gumstack_server | - | available | no | Manage your Postman collections, APIs, and workspaces. |
| privacy-com | Privacy.com | gumstack_server | - | available | no | Create and manage virtual payment cards with Privacy.com. |
| profound | Profound | gumstack_server | - | available | no | Track and optimize your brand visibility in AI answers with Profound. |
| pylon | Pylon | gumstack_server | - | available | no | Manage your Pylon support issues, accounts, and contacts. |
| quicknode | QuickNode | gumstack_server | - | available | no | Access blockchain data and node infrastructure with QuickNode. |
| ramp | Ramp | gumstack_server | - | available | no | Manage your Ramp cards, spend, bills, and transactions. |
| ramp-data | Ramp Data | gumstack_server | - | available | no | Query and analyze your Ramp spend and transaction data. |
| razorpay | Razorpay | gumstack_server | - | available | no | Manage your Razorpay payments, orders, and settlements. |
| read-ai | Read AI | gumstack_server | - | available | no | Access your Read AI meeting summaries and productivity insights. |
| ref | Ref | gumstack_server | - | available | no | Search up-to-date documentation for APIs, libraries, and services with Ref. |
| replit | Replit | gumstack_server | - | available | no | Build, run, and manage your Replit apps and projects. |
| rillet | Rillet | gumstack_server | - | available | no | Query your Rillet general ledger, accounting, and financials. |
| rocketlane | Rocketlane | gumstack_server | - | available | no | Manage your Rocketlane projects, tasks, and customer onboarding. |
| sandp-global | S&P Global | gumstack_server | - | available | no | Access S&P Global financial and market data. |
| sanity | Sanity | gumstack_server | - | available | no | Manage your Sanity content, documents, and datasets. |
| scholar-gateway | Scholar Gateway | gumstack_server | - | available | no | Search peer-reviewed research from Wiley journals with Scholar Gateway. |
| scite | Scite | gumstack_server | - | available | no | Analyze research citations and smart citations with Scite. |
| send | Send | gumstack_server | - | available | no | Create trackable documents and track viewer engagement with Send. |
| sentry | Sentry | gumstack_server | - | available | no | Investigate Sentry issues, errors, releases, and performance data. |
| shapes | Shapes | gumstack_server | - | available | no | Query your people and HR data with Shapes. |
| signnow | SignNow | gumstack_server | - | available | no | Send and manage e-signature documents with SignNow. |
| splice | Splice | gumstack_server | - | available | no | Search and access music samples and sounds on Splice. |
| stytch | Stytch | gumstack_server | - | available | no | Manage your Stytch authentication, users, and sessions. |
| sumble | Sumble | gumstack_server | - | available | no | Research company tech stacks, projects, and contacts with Sumble. |
| supabase | Supabase | gumstack_server | - | available | no | Manage Supabase projects, databases, branches, and logs. |
| superhuman-mail | Superhuman | gumstack_server | - | available | no | Access and manage your Superhuman email. |
| supermetrics-marketing-analytics | Supermetrics | gumstack_server | - | available | no | Pull and analyze cross-channel marketing data with Supermetrics. |
| swagger | Swagger | gumstack_server | - | available | no | Design and explore your Swagger and OpenAPI definitions. |
| sybill | Sybill | gumstack_server | - | available | no | Access your Sybill call summaries and sales insights. |
| synapse-org | Synapse | gumstack_server | - | available | no | Access research datasets and projects on Synapse. |
| synthesize-bio | Synthesize Bio | gumstack_server | - | available | no | Generate and explore genomic and gene expression data with Synthesize Bio. |
| tavily | Tavily | gumstack_server | - | available | no | Search the web and extract content with Tavily. |
| third-bridge | Third Bridge | gumstack_server | - | available | no | Access Third Bridge investment research and expert insights. |
| thoughtspot-spotter | ThoughtSpot Spotter | gumstack_server | - | available | no | Ask questions of your ThoughtSpot data with Spotter. |
| ticket-tailor | Ticket Tailor | gumstack_server | - | available | no | Manage your Ticket Tailor events, tickets, and orders. |
| tiktok-ads | TikTok Ads | gumstack_server | - | available | no | Manage your TikTok for Business ad campaigns, audiences, creatives, and reporting. |
| topcounsel-by-the-l-suite | TopCounsel by The L Suite | gumstack_server | - | available | no | Find and manage legal talent with TopCounsel by The L Suite. |
| trellis | Trellis | gumstack_server | - | available | no | Search state court records and litigation analytics with Trellis. |
| turquoise | Turquoise Health | gumstack_server | - | available | no | Access healthcare pricing, rates, and contract data with Turquoise Health. |
| udemy-business | Udemy Business | gumstack_server | - | available | no | Search and access Udemy Business courses and learning content. |
| unthread | Unthread | gumstack_server | - | available | no | Manage your Unthread support tickets and conversations. |
| unwrap | Unwrap | gumstack_server | - | available | no | Analyze customer feedback and product insights with Unwrap. |
| vibe-prospecting | Vibe Prospecting | gumstack_server | - | available | no | Find and enrich B2B leads and accounts with Explorium's Vibe Prospecting. |
| whimsical | Whimsical | gumstack_server | - | available | no | Create and manage Whimsical diagrams, flowcharts, and boards. |
| windsor-ai | Windsor.ai | gumstack_server | - | available | no | Pull and connect your marketing analytics data with Windsor.ai. |
| wix | Wix | gumstack_server | - | available | no | Manage your Wix sites, content, and store. |
| workable | Workable | gumstack_server | - | available | no | Manage your Workable jobs, candidates, and hiring pipeline. |
| yardi-matrix | Yardi Matrix | gumstack_server | - | available | no | Access Yardi Matrix commercial real estate data and analytics. |
| yardi-virtuoso | Yardi Virtuoso | gumstack_server | - | available | no | Query your Yardi property data and workflows with Virtuoso. |
| zapier | Zapier | gumstack_server | - | available | no | Trigger and run your Zapier automations across thousands of apps. |
| zip | Zip | gumstack_server | - | available | no | Manage Zip procurement requests, approvals, vendors, and spend. |
| zocks | Zocks | gumstack_server | - | available | no | Automate meeting notes, forms, and client data for financial advisors with Zocks. |
| alphaxiv | alphaXiv | gumstack_server | - | available | no | Search and explore research papers on alphaXiv. |
| imanage-work | iManage Work | gumstack_server | - | available | no | Access and manage your iManage documents and matters. |

**Status**: `connected` = ready to use, `available` = can be added, `blocked` = restricted by org policy.
