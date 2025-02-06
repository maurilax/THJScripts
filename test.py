import csv
import os
import re

def extract_date_from_line(line):
  """
  Extracts the date and time from a log line.

  Args:
    line: The log line string.

  Returns:
    A string containing the date and time, or None if no date is found.
  """
  try:
    # Example: [Mon Jan 27 01:11:14 2025]
    match = re.search(r"\[(.*?)\]", line)
    if match:
      return match.group(1)
    else:
      return None
  except Exception as e:
    print(f"Error extracting date from line: {e}")
    return None


def count_and_print_matched_lines_grouped(folder_path, target_phrases,
                                         output_csv_filename):
  """
  Counts partial line matches (case-insensitive) for a list of target phrases,
  groups by character name (starting with 'Mint'), prints the matches with
  counts, and writes the matched lines with character name and date to a CSV file.

  Args:
    folder_path: Path to the folder.
    target_phrases: A list of phrases to search for.
    output_csv_filename: Name of the output CSV file.
  """

  try:
    if not os.path.isdir(folder_path):
      print(f"Error: Folder '{folder_path}' not found.")
      return

    grouped_counts = {}
    total_count = 0

    with open(output_csv_filename, 'w', newline='',
              encoding='utf-8') as csvfile:
      csv_writer = csv.writer(csvfile)
      csv_writer.writerow(["Character", "Date", "Line"])  # Write header

      for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        if os.path.isfile(filepath):
          try:
            match = re.search(r"_(Mint[^_]+)_thj", filename)
            if match:
              character_name = match.group(1)
            else:
              character_name = None

            if character_name:
              with open(filepath, 'r', encoding='utf-8') as file:
                count = 0
                matched_lines = []
                for line in file:
                  for phrase in target_phrases:
                    if re.search(phrase, line, re.IGNORECASE):
                      count += 1

                      # Strip unwanted text before saving to CSV
                      line_to_save = line.strip()
                      line_to_save = re.sub(r"\[.*?\]", "",
                                            line_to_save)  # Remove date
                      line_to_save = re.sub(r"--You have looted a ", "",
                                            line_to_save)  # Remove loot message
                      line_to_save = re.sub(r".--", "",
                                            line_to_save)  # Remove trailing '--'

                      matched_lines.append(
                          line.strip())  # Original line for printing
                      date_str = extract_date_from_line(line)
                      if date_str:
                        csv_writer.writerow(
                            [character_name, date_str, line_to_save])
                      break

                if count > 0:
                  if character_name not in grouped_counts:
                    grouped_counts[character_name] = {
                        "total_character_count": 0
                    }

                  grouped_counts[character_name][filename] = {
                      "count": count,
                      "lines": matched_lines
                  }
                  grouped_counts[character_name][
                      "total_character_count"] += count
                  total_count += count
            else:
              print(
                  f"Warning: Could not extract character name (starting with 'Mint') from filename '{filename}'. Skipping."
              )

          except UnicodeDecodeError:
            print(f"Warning: Could not decode file '{filename}'. Skipping.")
          except Exception as e:
            print(f"Error reading file '{filename}': {e}. Skipping.")

    # Print the grouped counts and matched lines
    if grouped_counts:
      for character_name, file_data in grouped_counts.items():
        print(
            f"Character: {character_name} (Total: {file_data['total_character_count']})"
        )
        for filename, data in file_data.items():
          if filename!= "total_character_count":
            print(f"  File: {filename}, Count: {data['count']}")
            for line in data['lines']:
              print(f"    Matched Line: {line}")
      print(f"\nTotal count across all files: {total_count}")
    else:
      print("No files found with matching lines, or folder not found.")

  except Exception as e:
    print(f"A general error occurred: {e}")


# Example usage:
folder_path = r"C:\\Users\Joe\Desktop\Projects\THJLogsVelious\SourceLogs"

# List of target phrases with the loot message included
target_phrases = [
    "--You have looted a Abashi's Rod of Disempowerment",
    "--You have looted a Camii's Bracer of Vigor",
    "--You have looted a Sirran's Boots of Insanity",
    "--You have looted a Ssra's Bloodstone Eyepatch",
    "--You have looted a Jaelen's Katana",
    "--You have looted a Akkirus' Mask of Warfare",
    "--You have looted a Mrylokar's Dagger of Vengeance",
    "--You have looted a Tolan's Longsword of the Glade",
    "--You have looted a Hobart's War Helmet",
    "--You have looted a Do`Vassir's Gauntlets of Might",
    "--You have looted a Solist's Earring of Insight",
    "--You have looted a Rowyl's Metal Armguards",
    "--You have looted a Yakatizma's Shield of Crafting",
    "--You have looted a Crystasia's Crystal Ring",
    "--You have looted a Palladius' Axe of Slaughter",
    "--You have looted a Brother Xave's Headband",
    "--You have looted a Valtron's Necklace of Wonder",
    "--You have looted a Feeliux's Cord of Velocity",
    "--You have looted a Vyrinn's Earring of Insanity",
    "--You have looted a Kelsiferous' Armband of Artistry",
    "--You have looted a Maclaer's Boots of Silence",
    "--You have looted a Sal`Varae's Robe of Darkness",
    "--You have looted a Viik's Pauldrons of Pain",
    "--You have looted a Gharn's Rock of Smashing",
    "--You have looted a Prismatic Scale of"  # Added phrase
]

output_csv_filename = "matched_lines.csv"

count_and_print_matched_lines_grouped(folder_path, target_phrases,
                                     output_csv_filename)

print(f"Matched lines written to {output_csv_filename}")