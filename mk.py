import os
import re


def split_markdown(input_file, output_folder):
    """
    Split a Markdown file into multiple .md files based on the '##' chapter headings.
    Returns the course title and chapters for index generation.
    """

    # 1. Read all lines from the input markdown
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 2. Prepare output paths
    #    For example, if input_file is 'course/my_course.md' -> base_name = 'my_course'
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    #    The folder where the split markdown files go will be e.g. 'output/my_course'
    output_subfolder = os.path.join(output_folder, base_name)
    os.makedirs(output_subfolder, exist_ok=True)

    # 3. Keep track of chapters
    chapters = []  # Will store (chapter_number, chapter_title)
    current_chapter_lines = []
    current_chapter_title = None
    chapter_number = 0

    # 4. The first line might be the "main title" (e.g. "# My First Course")
    #    We'll store this to put it in the index.
    #    We don't *need* to treat the first line as special if you prefer not to.
    main_title = ""
    if lines and lines[0].startswith("# "):
        main_title = lines[0].replace("# ", "").strip()

    # 5. Helper function to write chapter to file
    def write_chapter(ch_num, ch_title, ch_lines):
        """Write the collected lines for a chapter to a new file."""
        # Example file name: chapter_1.md, chapter_2.md, etc.
        chapter_filename = f"lesson_{ch_num}.md"
        chapter_path = os.path.join(output_subfolder, chapter_filename)

        with open(chapter_path, "w", encoding="utf-8") as outfile:
            outfile.writelines(ch_lines)

        return chapter_filename

    # 6. Parse line-by-line
    for i, line in enumerate(lines):
        # Skip the first line if it's the main title (already stored),
        # but keep it in the final output for the "index" page's heading
        if i == 0 and main_title:
            continue

        # If we detect a "##" heading, that means a new chapter starts
        if line.startswith("## "):
            # If there's any existing chapter collected, write it out first
            if current_chapter_lines:
                filename = write_chapter(
                    chapter_number, current_chapter_title, current_chapter_lines
                )
                chapters.append((chapter_number, current_chapter_title, filename))

            # Start a new chapter
            chapter_number += 1
            # The line after '## ' should be the chapter title
            current_chapter_title = line.replace("## ", "").strip()
            current_chapter_lines = [line]  # Start this new chapter's content

        else:
            # Otherwise, keep adding lines to the current chapter
            if current_chapter_title:
                current_chapter_lines.append(line)

    # 7. After the loop, if there's an unfinished chapter, write it out
    if current_chapter_lines:
        filename = write_chapter(
            chapter_number, current_chapter_title, current_chapter_lines
        )
        chapters.append((chapter_number, current_chapter_title, filename))

    return main_title, chapters


def process_all_courses(courses_dir, output_dir):
    """Process all markdown files in the courses directory."""
    all_courses = []

    # Process each .md file in courses directory
    for filename in os.listdir(courses_dir):
        print("Found file: ", filename)
        if filename.endswith(".md"):
            input_file = os.path.join(courses_dir, filename)
            course_name = os.path.splitext(filename)[0]

            # Split the markdown and get course info
            main_title, chapters = split_markdown(input_file, output_dir)
            all_courses.append((main_title, course_name, chapters))

    # Create main index.md
    index_path = os.path.join("index.md")
    with open(index_path, "w", encoding="utf-8") as index_file:
        for course_title, course_name, chapters in all_courses:
            # Write course title
            index_file.write(f"# {course_title}\n\n")

            # List all chapters
            for ch_num, ch_title, ch_filename in chapters:
                index_file.write(
                    f"- [Lesson {ch_num}: {ch_title}](docs/{course_name}/{ch_filename})\n"
                )
            index_file.write("\n")


if __name__ == "__main__":
    courses_dir = "courses"
    output_dir = "docs"
    process_all_courses(courses_dir, output_dir)
    print("Done! Check the 'docs' folder for results.")
