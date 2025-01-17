import os
import re


def split_markdown(input_file, output_folder):
    """
    Split a Markdown file into multiple .md files based on the '##' chapter headings.
    Also create an index.md that references all chapters.
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

    # 8. Create the index.md in `output_folder`
    index_path = os.path.join(output_folder, "index.md")
    with open(index_path, "w", encoding="utf-8") as index_file:
        # Write the main title (if any), or a fallback
        if main_title:
            index_file.write(f"# {main_title}\n\n")
        else:
            index_file.write("# Course Index\n\n")

        # List all chapters
        for ch_num, ch_title, ch_filename in chapters:
            # We can write them as links: `[Chapter 1](my_course/chapter_1.md)`
            # Or simply list them. Adjust to your preference.

            # Example: `- [Chapter 1: Some Title](my_course/chapter_1.md)`
            index_file.write(
                f"- [Lesson {ch_num}: {ch_title}]({base_name}/{ch_filename})\n"
            )


if __name__ == "__main__":
    # Example usage:
    input_md = "courses/api-fundamentals.md"
    output_dir = "docs"
    split_markdown(input_md, output_dir)
    print("Done! Check the 'output' folder for results.")
