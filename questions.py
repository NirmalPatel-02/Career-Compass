FEATURE_META = {
    "logical_thinking": (0,2), "numerical_thinking": (0,2), "verbal_thinking": (0,2), "visual_thinking": (0,2),
    "likes_coding": (0,1), "likes_data": (0,1), "likes_design": (0,1), "likes_business": (0,1),
    "likes_writing": (0,1), "likes_security": (0,1), "people_oriented": (0,1), "system_oriented": (0,1),
    "research_oriented": (0,1), "risk_tolerance": (0,2),
    "backend_interest": (0,1), "frontend_interest": (0,1), "mobile_interest": (0,1), "game_interest": (0,1),
    "system_depth": (0,2), "ui_focus": (0,2), "performance_focus": (0,2),
    "statistics_interest": (0,2), "ml_interest": (0,2), "research_interest": (0,2), "business_context": (0,2),
    "model_deployment": (0,1), "data_cleaning": (0,2), "stakeholder_focus": (0,2), "data_driven": (0,2),
    "strategy_interest": (0,2), "execution_focus": (0,2), "communication_skill": (0,2),
    "visual_creativity": (0,2), "user_empathy": (0,2), "design_tools": (0,2), "research_focus": (0,2),
    "writing_skill": (0,2), "technical_depth": (0,2), "teaching_interest": (0,2), "marketing_orientation": (0,2),
    "community_engagement": (0,2), "automation_interest": (0,1), "security_focus": (0,2), 
    "system_reliability": (0,2), "testing_focus": (0,2)
}

DOMAIN_QUESTIONS = {
    0: {
        "likes_coding": "If you had to tell a computer step-by-step how to do a task, would you enjoy figuring out those steps?",
        "likes_data": "When you see numbers or information, do you enjoy finding meaning or patterns in them?",
        "likes_design": "When something looks confusing or messy, do you feel like improving how it looks or feels?",
        "likes_business": "When multiple solutions are possible, do you enjoy deciding which one makes the most sense overall?",
        "likes_writing": "Do you enjoy explaining ideas clearly so others can understand them?",
        "likes_security": "Do you often think about what could go wrong and how to prevent it?",
        "people_oriented": "Do you enjoy helping or working closely with other people?",
        "system_oriented": "Do you like understanding how different parts of something work together?",
        "research_oriented": "Do you enjoy asking ‘why’ and learning things in depth?"
    },
    1: {
        "likes_coding": "Do you enjoy building things using code?",
        "likes_data": "Do you enjoy working with numbers, patterns, or data?",
        "likes_design": "Do you enjoy creating visual designs or layouts?",
        "likes_business": "Do you enjoy planning, strategy, or decision-making?",
        "likes_writing": "Do you enjoy writing or explaining ideas clearly?",
        "likes_security": "Do you find system safety and security interesting?",
        "people_oriented": "Do you enjoy interacting with people as part of your work?",
        "system_oriented": "Do you enjoy working with complex systems?",
        "research_oriented": "Do you enjoy exploring new ideas or research?"
    }
}

SUB_DOMAIN_QUESTIONS = {
    "Technology & Engineering": {
        0: {
            "backend_interest": "If an app shows an error, would you rather figure out why it happened than change how it looks?",
            "frontend_interest": "Do you care more about how an app looks and feels than how it works inside?",
            "mobile_interest": "Do you prefer thinking about features mainly used on phones?",
            "game_interest": "Do you enjoy thinking about how games or interactive apps work?",
            "system_depth": "Do you enjoy focusing deeply on one problem until it is solved?",
            "ui_focus": "Do you notice when apps feel uncomfortable or confusing to use?",
            "performance_focus": "Do slow or laggy apps bother you enough to want to fix them?"
        },
        1: {
            "backend_interest": "Do you enjoy backend systems and APIs?",
            "frontend_interest": "Do you enjoy building user interfaces?",
            "mobile_interest": "Do you prefer mobile apps over websites?",
            "game_interest": "Do you enjoy games or real-time graphics?",
            "system_depth": "Do you like going deep into one system?",
            "ui_focus": "Do you care a lot about UI and user experience?",
            "performance_focus": "Do you care about performance and optimization?"
        }
    },
    "Data & AI": {
        0: {
            "statistics_interest": "When given lots of information, do you enjoy finding useful patterns in it?",
            "ml_interest": "Do you find it interesting when computers improve by learning from examples?",
            "research_interest": "Do you enjoy experimenting to see what works better?",
            "business_context": "Do you like using information to make smarter decisions?",
            "model_deployment": "After building something, do you care about people actually using it?",
            "data_cleaning": "Are you okay fixing messy or incomplete information?"
        },
        1: {
            "statistics_interest": "Do you enjoy statistics and math?",
            "ml_interest": "Are you interested in machine learning models?",
            "research_interest": "Do you enjoy research and experiments?",
            "business_context": "Do you like applying data to business problems?",
            "model_deployment": "Do you like deploying models to production?",
            "data_cleaning": "Do you enjoy cleaning and preparing data?"
        }
    },
    "Security & Infrastructure": {
        0: {
            "automation_interest": "Do you like setting things up so they work automatically without manual effort?",
            "security_focus": "Do you worry about misuse, hacks, or things going wrong in systems?",
            "system_reliability": "Do you care a lot if something breaks or stops working?",
            "testing_focus": "Do you like checking things to catch problems early?"
        },
        1: {
            "automation_interest": "Do you enjoy automating systems and pipelines?",
            "security_focus": "Are you interested in cybersecurity and threats?",
            "system_reliability": "Do you care about uptime and reliability?",
            "testing_focus": "Do you enjoy testing and validation?"
        }
    },
    "Business & Product": {
        0: {
            "stakeholder_focus": "Do you enjoy balancing different people’s expectations?",
            "data_driven": "Do you prefer using facts rather than guessing?",
            "strategy_interest": "Do you enjoy thinking ahead and planning outcomes?",
            "execution_focus": "Do you like seeing ideas turn into real results?",
            "communication_skill": "Are you comfortable explaining ideas clearly?"
        },
        1: {
            "stakeholder_focus": "Do you enjoy working with stakeholders?",
            "data_driven": "Do you like making decisions using data?",
            "strategy_interest": "Do you enjoy strategy and planning?",
            "execution_focus": "Do you enjoy executing plans end-to-end?",
            "communication_skill": "Are you confident in communication?"
        }
    },
    "Design & Creative": {
        0: {
            "visual_creativity": "Do you naturally think about how things should look?",
            "user_empathy": "Do you often think from another person’s point of view?",
            "design_tools": "Do you enjoy turning ideas into visuals or layouts?",
            "research_focus": "Do you like understanding why people behave a certain way?"
        },
        1: {
            "visual_creativity": "Do you consider yourself visually creative?",
            "user_empathy": "Do you enjoy understanding user needs?",
            "design_tools": "Are you comfortable with design tools?",
            "research_focus": "Do you enjoy design research?"
        }
    },
    "Writing & Content": {
        0: {
            "writing_skill": "Do you enjoy expressing ideas clearly in words?",
            "technical_depth": "Do you enjoy simplifying complex ideas for others?",
            "teaching_interest": "Do you like helping others learn?",
            "marketing_orientation": "Do you enjoy influencing people with words?",
            "community_engagement": "Do you enjoy engaging with groups or communities?"
        },
        1: {
            "writing_skill": "Do you enjoy writing structured content?",
            "technical_depth": "Do you like explaining technical concepts?",
            "teaching_interest": "Do you enjoy teaching others?",
            "marketing_orientation": "Do you enjoy persuasive writing?",
            "community_engagement": "Do you like engaging with communities?"
        }
    }
}