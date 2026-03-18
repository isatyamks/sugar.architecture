#!/usr/bin/env python3
"""
Synthetic dataset generator for AI reflection training.

Produces training examples that CLOSELY mirror real Sugar Journal data.
Based on actual data observed from Sugar's Datastore:

  Entry 1:  Title: TurtleBlocks Activity
            Bundle ID: (empty)
            MIME Type: application/x-turtle-art
            Timestamp: 1771791209
            Activity ID: c9cd5a475cf0ed4fbbde86da40b48bdecf46b82d

  Entry 2:  Title: Terminal Activity
            Bundle ID: (empty)
            MIME Type: text/plain
            Timestamp: 1771791201

  Entry 3:  Title: Screenshot of "Terminal Activity"
            MIME Type: image/png

Usage:
    python scripts/generate_dataset.py --output data/reflection_dataset.jsonl
    python scripts/generate_dataset.py --output data/reflection_dataset.jsonl --count 1000
"""

import json
import random
import hashlib
import uuid
import argparse
import os
from datetime import datetime, timedelta


# =============================================================
# REAL SUGAR ACTIVITIES
# These are the actual activities installed in Sugar OS,
# with their real bundle_ids, mime_types, and typical content
# =============================================================

SUGAR_ACTIVITIES = [
    {
        "bundle_id": "org.laptop.TurtleArtActivity",
        "activity_name": "Turtle Blocks",
        "mime_type": "application/x-turtle-art",
        "category": "programming",
        "typical_titles": [
            "TurtleBlocks Activity",
            "My Turtle Drawing",
            "Spiral Pattern",
            "Square Dance",
            "Rainbow Turtle",
            "Star Shape",
            "Flower Pattern",
            "My House Drawing",
            "Cool Shapes",
            "Turtle Maze",
            "Circle Art",
            "Tree Drawing",
            "Polygon Fun",
            "Colorful Spiral",
            "My First Program",
        ],
        "typical_descriptions": [
            "",
            "Made a spiral using repeat blocks",
            "Drew colorful shapes",
            "Learning about loops",
            "Experimenting with angles",
            "Used forward and right blocks",
        ],
    },
    {
        "bundle_id": "org.laptop.Write",
        "activity_name": "Write",
        "mime_type": "text/plain",
        "category": "writing",
        "typical_titles": [
            "My Story",
            "Write Activity",
            "My Family",
            "What I Did Today",
            "My Favorite Animal",
            "The Big Adventure",
            "School Report",
            "My Best Friend",
            "Letter to Mom",
            "Poem About Rain",
            "Science Notes",
            "Math Homework",
            "Daily Journal",
            "Book Report",
            "Creative Writing",
        ],
        "typical_descriptions": [
            "",
            "A story about my dog",
            "Notes from class",
            "Writing practice",
            "My diary entry",
            "Homework assignment",
        ],
    },
    {
        "bundle_id": "org.laptop.Pippy",
        "activity_name": "Pippy",
        "mime_type": "text/x-python",
        "category": "programming",
        "typical_titles": [
            "Pippy Activity",
            "My Python Code",
            "Hello World",
            "Number Game",
            "Calculator",
            "Guess the Number",
            "Simple Quiz",
            "Drawing with Code",
            "Math Helper",
            "My First Script",
            "Pattern Maker",
            "Color Picker",
        ],
        "typical_descriptions": [
            "",
            "Learning Python",
            "Made a number guessing game",
            "Calculator program",
            "Practice coding",
        ],
    },
    {
        "bundle_id": "org.laptop.Paint",
        "activity_name": "Paint",
        "mime_type": "image/png",
        "category": "art",
        "typical_titles": [
            "My Drawing",
            "Paint Activity",
            "My Family Portrait",
            "Sunset Painting",
            "My Pet",
            "Flowers",
            "My School",
            "Landscape",
            "Abstract Art",
            "My House",
            "Self Portrait",
            "Rainbow",
            "My Friend",
            "Animal Drawing",
            "Nature Scene",
        ],
        "typical_descriptions": [
            "",
            "Drew my family",
            "A picture of my school",
            "Using different colors",
            "Practicing drawing",
            "Art project",
        ],
    },
    {
        "bundle_id": "org.laptop.Calculate",
        "activity_name": "Calculate",
        "mime_type": "text/plain",
        "category": "math",
        "typical_titles": [
            "Calculate Activity",
            "Math Practice",
            "Addition Problems",
            "Multiplication Table",
            "Fractions",
            "Math Homework",
            "Number Explorer",
            "Division Practice",
            "Geometry Calculations",
        ],
        "typical_descriptions": [
            "",
            "Practicing multiplication",
            "Solving math problems",
            "Learning fractions",
        ],
    },
    {
        "bundle_id": "org.laptop.Browse",
        "activity_name": "Browse",
        "mime_type": "text/html",
        "category": "research",
        "typical_titles": [
            "Browse Activity",
            "Research Project",
            "Science Research",
            "History Homework",
            "Wikipedia Reading",
            "Learning About Animals",
            "Geography Research",
            "Looking Up Words",
        ],
        "typical_descriptions": [
            "",
            "Researching for my project",
            "Reading about science",
            "Looking things up",
        ],
    },
    {
        "bundle_id": "org.laptop.Record",
        "activity_name": "Record",
        "mime_type": "audio/ogg",
        "category": "media",
        "typical_titles": [
            "Record Activity",
            "My Recording",
            "Song Practice",
            "Interview",
            "Sound Effects",
            "My Voice",
            "Reading Aloud",
            "Music Recording",
        ],
        "typical_descriptions": [
            "",
            "Recorded myself reading",
            "Made a sound clip",
            "Practicing singing",
        ],
    },
    {
        "bundle_id": "org.laptop.Memorize",
        "activity_name": "Memorize",
        "mime_type": "application/x-memorize-project",
        "category": "game",
        "typical_titles": [
            "Memorize Activity",
            "Memory Game",
            "Matching Cards",
            "Word Match",
            "Picture Match",
            "Animal Matching",
        ],
        "typical_descriptions": [
            "",
            "Playing memory game",
            "Matching practice",
        ],
    },
    {
        "bundle_id": "org.sugarlabs.Musicblocks",
        "activity_name": "Music Blocks",
        "mime_type": "application/x-music-blocks",
        "category": "music",
        "typical_titles": [
            "Music Blocks Activity",
            "My Song",
            "Beat Maker",
            "Rhythm Pattern",
            "Simple Melody",
            "Music Experiment",
            "Drum Pattern",
            "My Composition",
        ],
        "typical_descriptions": [
            "",
            "Making a melody",
            "Experimenting with beats",
            "Learning about rhythm",
        ],
    },
    {
        "bundle_id": "org.laptop.Maze",
        "activity_name": "Maze",
        "mime_type": "application/x-maze",
        "category": "game",
        "typical_titles": [
            "Maze Activity",
            "Maze Challenge",
            "Hard Maze",
            "Speed Run",
        ],
        "typical_descriptions": [
            "",
            "Solving mazes",
            "Trying harder levels",
        ],
    },
    {
        "bundle_id": "org.laptop.Chat",
        "activity_name": "Chat",
        "mime_type": "text/plain",
        "category": "communication",
        "typical_titles": [
            "Chat Activity",
            "Group Chat",
            "Class Discussion",
            "Chat with Friends",
        ],
        "typical_descriptions": [
            "",
            "Talking with classmates",
            "Group discussion",
        ],
    },
]

# Screenshots (no bundle_id, as seen in real data)
SCREENSHOT_TEMPLATES = [
    "Screenshot of \"Terminal Activity\"",
    "Screenshot of \"TurtleBlocks Activity\"",
    "Screenshot of \"Write Activity\"",
    "Screenshot of \"Paint Activity\"",
    "Screenshot of \"Browse Activity\"",
    "Screenshot of \"Pippy Activity\"",
    "Screenshot of \"Calculate Activity\"",
]


# =============================================================
# REFLECTIVE FRAMEWORKS AND THEIR PROMPTS
# Based on the 3 implemented frameworks
# =============================================================

FRAMEWORKS = {
    "gibbs": {
        "name": "Gibbs Reflective Cycle",
        "stages": {
            "description": {
                "intent": "Elicit factual recall of what happened",
                "prompts": {
                    "programming": [
                        "You worked on '{title}' in {activity} for {duration}. Can you walk me through what you built step by step?",
                        "Tell me about the program you made in '{title}'. What does it do?",
                        "You just finished '{title}'. Describe what your code does from start to finish.",
                        "What exactly did you create in '{title}' today? Walk me through it.",
                    ],
                    "writing": [
                        "You wrote '{title}' in {activity}. What is your writing about?",
                        "Tell me about '{title}'. What story or ideas are you sharing?",
                        "You spent {duration} writing '{title}'. What did you write about?",
                        "Describe what you wrote in '{title}'. Who or what is it about?",
                    ],
                    "art": [
                        "You created '{title}' in {activity}. Can you describe your picture to me?",
                        "Tell me about your drawing '{title}'. What did you include in it?",
                        "You spent {duration} on '{title}'. Describe what your artwork looks like.",
                        "What did you draw in '{title}'? Walk me through the different parts.",
                    ],
                    "math": [
                        "You worked on '{title}' in {activity}. What math problems did you solve?",
                        "Tell me about your math work in '{title}'. What types of problems did you do?",
                        "You spent {duration} on '{title}'. What math concepts were you working on?",
                    ],
                    "default": [
                        "You just finished '{title}' in {activity}. Can you describe what you did?",
                        "Tell me about your work on '{title}'. What happened during this session?",
                        "You spent {duration} on '{title}'. Walk me through what you did.",
                    ],
                },
            },
            "feelings": {
                "intent": "Explore emotional response to the experience",
                "prompts": {
                    "programming": [
                        "How did you feel while coding '{title}'? Were there moments of frustration or excitement?",
                        "What emotions came up while you were programming '{title}'? Was anything surprising?",
                        "When you were working on '{title}', what was the most exciting part? What was the most frustrating?",
                    ],
                    "writing": [
                        "How did you feel while writing '{title}'? Did your feelings change as you wrote?",
                        "What emotions did you experience while working on '{title}'?",
                        "Was there a part of writing '{title}' that made you feel really good? Or really stuck?",
                    ],
                    "art": [
                        "How did you feel while creating '{title}'? What was the most enjoyable part?",
                        "What feelings were you trying to express in '{title}'? How do you feel about how it turned out?",
                        "While drawing '{title}', were there moments when you felt stuck or when things just flowed?",
                    ],
                    "default": [
                        "How did you feel while working on '{title}'? Were there ups and downs?",
                        "What emotions did you notice during your time on '{title}'?",
                        "Was there a moment while doing '{title}' that stood out emotionally?",
                    ],
                },
            },
            "evaluation": {
                "intent": "Judge what went well and what didn't",
                "prompts": {
                    "programming": [
                        "Looking at '{title}', what parts of your code work really well? What could be better?",
                        "What went well while building '{title}'? What didn't go as planned?",
                        "If you had to grade your work on '{title}', what would you be proud of? What needs improvement?",
                    ],
                    "writing": [
                        "Looking at '{title}', which parts are you most proud of? Which parts could be stronger?",
                        "What works well in your writing '{title}'? What would you like to improve?",
                    ],
                    "art": [
                        "Looking at '{title}', what parts of your artwork do you like most? What would you change?",
                        "What turned out well in '{title}'? Is there anything you wish looked different?",
                    ],
                    "default": [
                        "What went well in '{title}'? What didn't work out as you hoped?",
                        "What are you most proud of in '{title}'? What could be improved?",
                    ],
                },
            },
            "analysis": {
                "intent": "Make sense of the experience",
                "prompts": {
                    "programming": [
                        "Why do you think some parts of '{title}' were easier to code than others?",
                        "What patterns did you notice while building '{title}'? Did any strategies help you solve problems?",
                    ],
                    "writing": [
                        "Why did you choose to write about this topic in '{title}'? What influenced your choices?",
                        "What helped you when you got stuck while writing '{title}'? What made the hard parts hard?",
                    ],
                    "art": [
                        "Why did you choose these colors and shapes in '{title}'? What influenced your artistic choices?",
                        "What did you learn about drawing while creating '{title}'?",
                    ],
                    "default": [
                        "Why do you think '{title}' went the way it did? What factors made a difference?",
                        "What helped you succeed in '{title}'? What made the challenging parts difficult?",
                    ],
                },
            },
            "conclusion": {
                "intent": "Determine what was learned",
                "prompts": {
                    "programming": [
                        "What did you learn from building '{title}'? What new skill or concept did you pick up?",
                        "After finishing '{title}', what do you know now about programming that you didn't know before?",
                    ],
                    "writing": [
                        "What did you learn about writing from creating '{title}'?",
                        "After finishing '{title}', what's one thing you now understand better about expressing your ideas?",
                    ],
                    "art": [
                        "What did you learn about art or drawing from creating '{title}'?",
                        "After finishing '{title}', what's one new thing you discovered about making art?",
                    ],
                    "default": [
                        "What's the biggest thing you learned from doing '{title}'?",
                        "If you could tell a friend one thing you learned from '{title}', what would it be?",
                    ],
                },
            },
            "action_plan": {
                "intent": "Plan future action based on the experience",
                "prompts": {
                    "programming": [
                        "Next time you code something like '{title}', what will you do differently?",
                        "Based on what you learned from '{title}', what would you like to try building next?",
                    ],
                    "writing": [
                        "Next time you write something like '{title}', what will you do differently?",
                        "After working on '{title}', what kind of writing would you like to try next?",
                    ],
                    "art": [
                        "Next time you draw something like '{title}', what techniques will you try?",
                        "Based on '{title}', what would you like to create next?",
                    ],
                    "default": [
                        "Next time you do something like '{title}', what will you do differently?",
                        "What's your plan for continuing or building on '{title}'?",
                    ],
                },
            },
        },
    },
    "kolb": {
        "name": "Kolb Experiential Learning Cycle",
        "stages": {
            "concrete_experience": {
                "intent": "Focus on what the learner did (the experience itself)",
                "prompts": {
                    "programming": [
                        "You just worked on '{title}' in {activity}. Tell me about the experience — what did you actually do?",
                        "Walk me through your experience coding '{title}'. What steps did you take?",
                    ],
                    "writing": [
                        "You just wrote '{title}'. Tell me about the experience of writing it. What was it like?",
                        "Describe your experience of writing '{title}'. How did the process go?",
                    ],
                    "art": [
                        "You just created '{title}'. Tell me about the experience of making it.",
                        "Describe what it was like to create '{title}'. What was your process?",
                    ],
                    "default": [
                        "You just finished '{title}'. What was the experience like?",
                        "Describe your experience doing '{title}' in your own words.",
                    ],
                },
            },
            "reflective_observation": {
                "intent": "Focus on what the learner noticed and observed",
                "prompts": {
                    "programming": [
                        "Looking back at '{title}', what did you notice about how your code works?",
                        "What surprised you while working on '{title}'? What did you observe that was unexpected?",
                    ],
                    "writing": [
                        "Looking back at '{title}', what do you notice about your writing style or choices?",
                        "Read through '{title}' again. What stands out to you now?",
                    ],
                    "art": [
                        "Step back and look at '{title}'. What do you notice about your artwork?",
                        "Looking at '{title}' now, what do you observe about the colors, shapes, or composition?",
                    ],
                    "default": [
                        "Looking back, what did you notice while working on '{title}'?",
                        "What observations stand out to you most about '{title}'?",
                    ],
                },
            },
            "abstract_conceptualization": {
                "intent": "Focus on patterns, theories, and general principles",
                "prompts": {
                    "programming": [
                        "Based on '{title}', what general rules or patterns have you noticed about programming?",
                        "What principle or concept from '{title}' could you apply to other coding projects?",
                    ],
                    "writing": [
                        "Based on writing '{title}', what general ideas about writing have you formed?",
                        "What did '{title}' teach you that applies to all writing, not just this piece?",
                    ],
                    "art": [
                        "Based on creating '{title}', what general ideas about art or design have you formed?",
                        "What principle from '{title}' could you use in any other artwork?",
                    ],
                    "default": [
                        "Based on '{title}', what general idea or rule have you figured out?",
                        "What did '{title}' teach you that you could apply to other projects?",
                    ],
                },
            },
            "active_experimentation": {
                "intent": "Focus on planning to try something new",
                "prompts": {
                    "programming": [
                        "Based on what you learned from '{title}', what experiment or new feature would you like to try?",
                        "How could you test or extend what you built in '{title}'? What would you try differently?",
                    ],
                    "writing": [
                        "Based on what you learned writing '{title}', what new writing experiment would you try?",
                        "How could you test a different approach to the ideas in '{title}'?",
                    ],
                    "art": [
                        "Based on '{title}', what new artistic technique or style would you like to experiment with?",
                        "How could you take what you did in '{title}' further? What variation would you try?",
                    ],
                    "default": [
                        "Based on '{title}', what would you like to experiment with next?",
                        "How could you test or extend what you did in '{title}'?",
                    ],
                },
            },
        },
    },
    "what_so_what": {
        "name": "What? So What? Now What?",
        "stages": {
            "what": {
                "intent": "Describe what happened in simple terms",
                "prompts": {
                    "programming": [
                        "What did you make in '{title}'? Tell me about it!",
                        "You worked on '{title}' — what does your program do?",
                        "Tell me about '{title}'. What did you build today?",
                    ],
                    "writing": [
                        "What did you write about in '{title}'? Tell me!",
                        "You wrote '{title}' — what's it about?",
                        "Tell me about '{title}'. What did you write today?",
                    ],
                    "art": [
                        "What did you draw in '{title}'? Tell me about your picture!",
                        "You made '{title}' — what does it show?",
                        "Tell me about '{title}'. What did you create today?",
                    ],
                    "math": [
                        "What math did you work on in '{title}'?",
                        "Tell me about '{title}'. What numbers or problems did you work with?",
                    ],
                    "default": [
                        "What did you do in '{title}'? Tell me about it!",
                        "You finished '{title}' — what did you work on?",
                        "Tell me about '{title}'. What happened?",
                    ],
                },
            },
            "so_what": {
                "intent": "Why it matters, what was learned",
                "prompts": {
                    "programming": [
                        "That's cool! Why is '{title}' important to you? What did you learn from making it?",
                        "Nice work on '{title}'! What did you learn while coding it?",
                        "So what did you figure out while building '{title}'?",
                    ],
                    "writing": [
                        "Nice writing! Why did you choose to write about this in '{title}'? What did you learn?",
                        "So what makes '{title}' important? What did you discover while writing it?",
                    ],
                    "art": [
                        "Cool drawing! Why did you choose to draw this in '{title}'? What did you learn?",
                        "So what makes '{title}' special to you? What did you figure out while creating it?",
                    ],
                    "default": [
                        "Why does '{title}' matter? What did you learn from it?",
                        "So what! What's the big takeaway from '{title}'?",
                        "What did working on '{title}' teach you?",
                    ],
                },
            },
            "now_what": {
                "intent": "What will you do next?",
                "prompts": {
                    "programming": [
                        "Now that you've made '{title}', what will you build next?",
                        "What's your next step after '{title}'? Any new ideas?",
                        "If you could keep working on '{title}', what would you add or change?",
                    ],
                    "writing": [
                        "Now that you've written '{title}', what will you write next?",
                        "What's your next step after '{title}'? Will you continue this story?",
                    ],
                    "art": [
                        "Now that you've drawn '{title}', what will you create next?",
                        "What's your next art project after '{title}'? Any new ideas?",
                    ],
                    "default": [
                        "Now what? What will you do next after '{title}'?",
                        "What's your next step after finishing '{title}'?",
                        "If you could keep going with '{title}', what would you do?",
                    ],
                },
            },
        },
    },
}

# History-aware prompt additions
HISTORY_AWARE_PREFIXES = {
    "returning_with_reflection": [
        "Last time you worked on '{prev_title}', you said: '{prev_reflection}'. ",
        "You previously reflected on '{prev_title}' and mentioned: '{prev_reflection}'. ",
        "Earlier, after working on '{prev_title}', you told me: '{prev_reflection}'. ",
    ],
    "returning_no_reflection": [
        "You've done {history_count} similar {activity} projects before, including '{prev_title}'. ",
        "I see you've used {activity} {history_count} times before. Last time you made '{prev_title}'. ",
        "This isn't your first time with {activity} — you also made '{prev_title}' before. ",
    ],
}

# Sample learner reflections (for history context)
SAMPLE_REFLECTIONS = [
    "I liked using the colors",
    "It was hard but I figured it out",
    "I learned about loops today",
    "The drawing didn't turn out how I wanted",
    "I need more practice with this",
    "I was really proud of my work",
    "I want to try something harder next time",
    "I used new blocks I hadn't tried before",
    "Writing was easier than last time",
    "I got stuck on one part but kept trying",
    "My friend helped me with an idea",
    "I want to add more details next time",
    "I learned how to use a new tool",
    "It was fun working on this",
    "I made fewer mistakes than last time",
]


def generate_activity_id():
    """Generate a realistic Sugar activity_id (40-char hex)."""
    return hashlib.sha1(
        str(uuid.uuid4()).encode()
    ).hexdigest()


def generate_uid():
    """Generate a realistic Sugar UID (UUID format)."""
    return str(uuid.uuid4())


def generate_timestamp(days_ago=0):
    """Generate a realistic Unix timestamp."""
    base = datetime(2026, 2, 23, 12, 0, 0)
    dt = base - timedelta(days=days_ago, hours=random.randint(0, 12))
    return int(dt.timestamp())


def generate_duration():
    """Generate a realistic session duration in seconds."""
    # Most activities: 5-45 minutes
    return random.choice([
        random.randint(300, 600),      # 5-10 min (quick)
        random.randint(600, 1200),     # 10-20 min (normal)
        random.randint(1200, 2700),    # 20-45 min (long)
        random.randint(2700, 5400),    # 45-90 min (very long, rare)
        0,                             # unknown (as seen in real data)
    ])


def generate_history(activity, count):
    """Generate realistic past history entries."""
    history = []
    for i in range(count):
        has_reflection = random.random() < 0.3  # 30% have reflections
        entry = {
            "title": random.choice(activity["typical_titles"]),
            "description": random.choice(activity["typical_descriptions"]),
            "timestamp": generate_timestamp(days_ago=random.randint(1, 60)),
            "reflection": random.choice(SAMPLE_REFLECTIONS) if has_reflection else None,
        }
        history.append(entry)
    return history


def pick_age():
    """Pick a realistic learner age."""
    return random.choice([
        random.randint(6, 8),    # young learner
        random.randint(9, 11),   # mid learner
        random.randint(12, 16),  # older learner
    ])


def format_duration(seconds):
    """Format seconds into human-readable duration."""
    if seconds == 0:
        return "some time"
    minutes = seconds // 60
    if minutes < 1:
        return "less than a minute"
    if minutes == 1:
        return "about a minute"
    if minutes < 60:
        return "{} minutes".format(minutes)
    hours = minutes // 60
    remaining = minutes % 60
    if remaining == 0:
        return "{} hour{}".format(hours, "s" if hours > 1 else "")
    return "{} hour{} and {} minutes".format(
        hours, "s" if hours > 1 else "", remaining
    )


def select_framework_for_age(age):
    """Select the most appropriate framework for the learner's age."""
    if age < 10:
        return "what_so_what"
    elif age < 12:
        return random.choice(["what_so_what", "kolb"])
    else:
        return random.choice(["kolb", "gibbs"])


def generate_one_example():
    """Generate a single training example."""

    # --- Activity context (mirrors real Journal data) ---
    is_screenshot = random.random() < 0.1  # 10% screenshots
    
    if is_screenshot:
        activity = random.choice(SUGAR_ACTIVITIES)
        title = random.choice(SCREENSHOT_TEMPLATES)
        bundle_id = ""
        activity_id = ""
        mime_type = "image/png"
        category = "art"
    else:
        activity = random.choice(SUGAR_ACTIVITIES)
        title = random.choice(activity["typical_titles"])
        bundle_id = activity["bundle_id"]
        activity_id = generate_activity_id()
        mime_type = activity["mime_type"]
        category = activity["category"]

    uid = generate_uid()
    duration_seconds = generate_duration()
    timestamp = generate_timestamp(days_ago=random.randint(0, 3))
    description = random.choice(activity["typical_descriptions"])

    # --- History (0-5 past entries) ---
    history_count = random.choices(
        [0, 1, 2, 3, 4, 5],
        weights=[30, 25, 20, 12, 8, 5],  # most learners have 0-2
    )[0]
    history = generate_history(activity, history_count)

    # --- Learner ---
    age = pick_age()
    framework_name = select_framework_for_age(age)
    framework = FRAMEWORKS[framework_name]

    # --- Pick stage ---
    stages = list(framework["stages"].keys())
    stage = random.choice(stages)
    stage_data = framework["stages"][stage]

    # --- Generate prompt ---
    prompt_category = category if category in stage_data["prompts"] else "default"
    prompt_template = random.choice(stage_data["prompts"][prompt_category])

    duration_str = format_duration(duration_seconds)

    # Build the prompt with context
    prompt = prompt_template.format(
        title=title,
        activity=activity["activity_name"],
        duration=duration_str,
    )

    # Add history-aware prefix if applicable
    if history_count > 0:
        prev = history[0]
        prev_title = prev["title"]
        prev_reflection = prev.get("reflection")

        if prev_reflection:
            prefix_templates = HISTORY_AWARE_PREFIXES["returning_with_reflection"]
        else:
            prefix_templates = HISTORY_AWARE_PREFIXES["returning_no_reflection"]

        prefix = random.choice(prefix_templates).format(
            prev_title=prev_title,
            prev_reflection=prev_reflection or "",
            history_count=history_count,
            activity=activity["activity_name"],
        )
        prompt = prefix + prompt

    # --- Build the full training example ---
    example = {
        # Input: Activity context (what Sugar sends)
        "input": {
            "context": {
                "activity_id": activity_id,
                "bundle_id": bundle_id,
                "title": title,
                "description": description,
                "mime_type": mime_type,
                "tags": [],
                "duration_seconds": duration_seconds if duration_seconds > 0 else None,
            },
            "learner": {
                "age": age,
                "language": "en",
            },
            "history": history,
        },
        # Output: What the LLM should generate
        "output": {
            "prompt_text": prompt,
            "framework_used": framework_name,
            "stage": stage,
            "stage_intent": stage_data["intent"],
            "model_version": "synthetic-v1",
        },
        # Metadata for training
        "metadata": {
            "activity_name": activity["activity_name"],
            "category": category,
            "history_count": history_count,
            "age_group": "young" if age < 10 else ("mid" if age < 13 else "older"),
        },
    }

    return example


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic reflection training dataset"
    )
    parser.add_argument(
        "--output", "-o",
        default="data/reflection_dataset.jsonl",
        help="Output file path (JSONL format)",
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=500,
        help="Number of examples to generate",
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=42,
        help="Random seed for reproducibility",
    )
    args = parser.parse_args()

    random.seed(args.seed)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    examples = []
    framework_counts = {}
    stage_counts = {}
    category_counts = {}

    for _ in range(args.count):
        example = generate_one_example()
        examples.append(example)

        # Track stats
        fw = example["output"]["framework_used"]
        st = example["output"]["stage"]
        cat = example["metadata"]["category"]
        framework_counts[fw] = framework_counts.get(fw, 0) + 1
        stage_counts[st] = stage_counts.get(st, 0) + 1
        category_counts[cat] = category_counts.get(cat, 0) + 1

    # Write JSONL
    with open(args.output, "w", encoding="utf-8") as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")

    # Also write a readable JSON sample
    sample_path = args.output.replace(".jsonl", "_sample.json")
    with open(sample_path, "w", encoding="utf-8") as f:
        json.dump(examples[:5], f, indent=2, ensure_ascii=False)

    # Print stats
    print("=" * 55)
    print("  SYNTHETIC DATASET GENERATED")
    print("=" * 55)
    print(f"\n  Total examples: {len(examples)}")
    print(f"  Output:         {args.output}")
    print(f"  Sample:         {sample_path}")
    print(f"\n  Framework distribution:")
    for fw, count in sorted(framework_counts.items()):
        print(f"    {fw:20s} {count:4d} ({100*count/len(examples):.1f}%)")
    print(f"\n  Stage distribution:")
    for st, count in sorted(stage_counts.items()):
        print(f"    {st:30s} {count:4d}")
    print(f"\n  Activity category distribution:")
    for cat, count in sorted(category_counts.items()):
        print(f"    {cat:20s} {count:4d} ({100*count/len(examples):.1f}%)")
    print(f"\n  Average history depth: {sum(e['metadata']['history_count'] for e in examples)/len(examples):.1f}")
    print("=" * 55)


if __name__ == "__main__":
    main()
