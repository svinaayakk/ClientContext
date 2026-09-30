from src.llm import analyze_meeting
from evaluation.ground_truth import GROUND_TRUTH


def normalize(text):
    return (
        text.lower()
        .strip()
        .replace(".", "")
        .replace(",", "")
    )


def contains_match(expected, actual):
    """
    Check whether an expected concept is represented
    in an extracted item.
    """

    expected = normalize(expected)
    actual = normalize(actual)

    return expected in actual or actual in expected


def evaluate_recall(expected_items, actual_items):
    """
    Measure how many expected concepts were extracted.
    """

    if not expected_items:
        return 1.0

    matched = 0
    used_actual = set()

    for expected in expected_items:

        for index, actual in enumerate(actual_items):

            if index in used_actual:
                continue

            if contains_match(expected, actual):
                matched += 1
                used_actual.add(index)
                break

    return matched / len(expected_items)


def evaluate_unsupported(actual_items, unsupported_items):
    """
    Measure how many known unsupported concepts were extracted.
    """

    if not unsupported_items:
        return 0.0

    detected = 0

    for unsupported in unsupported_items:

        for actual in actual_items:

            if contains_match(unsupported, actual):
                detected += 1
                break

    return detected / len(unsupported_items)


def evaluate_meeting(meeting_name, actual):

    expected = GROUND_TRUTH[meeting_name]

    fields = [
        "pain_points",
        "requirements",
        "objections",
        "action_items",
        "stakeholders"
    ]

    results = {}

    for field in fields:

        expected_items = expected.get(field, [])
        actual_items = getattr(actual, field, [])

        results[field] = evaluate_recall(
            expected_items,
            actual_items
        )

    unsupported_items = expected.get(
        "unsupported_extractions",
        []
    )

    all_extracted_items = []

    for field in fields:
        all_extracted_items.extend(
            getattr(actual, field, [])
        )

    unsupported_rate = evaluate_unsupported(
        all_extracted_items,
        unsupported_items
    )

    results["unsupported_extraction_rate"] = unsupported_rate

    return results


def print_results(meeting_name, results):

    print(f"\n===== {meeting_name.upper()} EVALUATION =====")

    for field, score in results.items():

        print(
            f"{field.upper()}: {score:.2f}"
        )


def main():

    for meeting_name in GROUND_TRUTH:

        transcript_path = (
            f"data/transcripts/{meeting_name}.txt"
        )

        with open(transcript_path, "r") as file:
            transcript = file.read()

        print(f"\nAnalyzing {meeting_name}...")

        actual = analyze_meeting(transcript)

        results = evaluate_meeting(
            meeting_name,
            actual
        )

        print_results(
            meeting_name,
            results
        )


if __name__ == "__main__":
    main()