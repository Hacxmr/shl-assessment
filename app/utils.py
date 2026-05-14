import re



# FORMAT RETRIEVAL CONTEXT


def format_context(items):

    blocks = []

    for i, item in enumerate(items):

        description = item.get(
            "description",
            ""
        )

        description = description[:1000]

        block = f"""
[{i + 1}]

Assessment Name:
{item.get("name", "")}

Assessment Type:
{item.get("test_type", "")}

URL:
{item.get("url", "")}

Job Levels:
{item.get("job_levels", "")}

Remote Support:
{item.get("remote", "")}

Adaptive:
{item.get("adaptive", "")}

Description:
{description}
"""

        blocks.append(block)

    return "\n".join(blocks)



# BUILD CONVERSATION STRING


def build_conversation(messages):

    lines = []

    for message in messages:

        role = message.role.upper()

        content = message.content.strip()

        lines.append(
            f"{role}: {content}"
        )

    return "\n".join(lines)



# COMPARISON QUERY PARSER


def parse_compare_query(text):

    text = text.lower()

    patterns = [

        r"compare (.+) and (.+)",

        r"compare (.+) vs (.+)",

        r"compare (.+) versus (.+)",

        r"difference between (.+) and (.+)",

        r"how is (.+) different from (.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            left = match.group(1).strip()

            right = match.group(2).strip()

            return left, right

    return None



# SAFE STRING CLEANING


def clean_text(text):

    text = text.strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text



# LIMIT RESPONSE LENGTH


def truncate_text(
    text,
    max_chars=1200
):

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "..."

