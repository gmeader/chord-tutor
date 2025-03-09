# Displays a chord to practice and
# Shows chords being played oin MIDI input
import random
import pygame
import checkbox
import mido
from music21 import chord, interval

# initial filters
show_inversions = False
show_accidentals = False
show_minor = False
show_major = True
show_7ths = True

midi_enabled = False
input_device_names = mido.get_input_names()
print(input_device_names)
if len(input_device_names):
  inport = mido.open_input(input_device_names[0])
  midi_enabled = True
else:
  print ("No MIDI inout devices found")
  midi_enabled = False


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255,0, 0)

note_names = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
# Define the list of chords to prompt
words = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
scales = ["Maj","min"]
inversions = ["","1st","2nd"]
sevenths = ["","7","Maj7"]
active_notes = []
newNote = True
# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 500
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
boxes = []
boxes.append( checkbox.Checkbox(screen, 1, 2, caption='Major'))
boxes.append( checkbox.Checkbox(screen, 75, 2, caption='Minor'))
boxes.append( checkbox.Checkbox(screen, 150, 2, caption='Accidentals'))
boxes.append( checkbox.Checkbox(screen, 270, 2, caption='Inversions'))
boxes.append( checkbox.Checkbox(screen, 380, 2, caption='Sevenths'))

boxes[0].checked = show_major
boxes[1].checked = show_minor
boxes[2].checked = show_accidentals
boxes[3].checked = show_inversions
boxes[4].checked = show_7ths

# Set the window title
pygame.display.set_caption("Random Chord Display")

# Define the font
font = pygame.font.SysFont(None, 100)
small_font = pygame.font.SysFont(None, 40)

cb_outline_color = (78, 137, 202)
check_color = (22, 61, 105)
cb_font_size = 25
cb_font_color = (39, 111, 191)
cb_text_offset = (28, 1)
cb_font = "Open Sans"

# Function to convert MIDI note number to note name
def get_note_name(note_number):
  octave = int(note_number / 12) - 1
  note = note_names[note_number % 12]
  #return f"{note}{octave}"
  return f"{note}"

def display_chord(notes):
  notes.sort()
  chord_string = midi_notes_to_chord(notes)
  notes_string =''
  for note_number in notes:
    notes_string += get_note_name(note_number)+' '
  #print(chord_string)
  display_notes(notes_string,chord_string)

# Function to display the prompt chord word on the screen
def display_word():
  current_word = random.choice(words)
  current_scale = random.choice(scales)
  # check for accidentals
  if show_accidentals == False:
    while ('#' in current_word) or ('b' in current_word):
      current_word = random.choice(words)

  if show_major:
    current_scale = "Maj"

  if show_minor:
    current_scale = "min"

  if show_minor and show_major:
    current_scale = random.choice(scales)

  if show_inversions:
    current_inversion = random.choice(inversions)
  else:
    current_inversion = ""

  if show_7ths:
    current_seventh = random.choice(sevenths)
    if current_scale == "Maj" and current_seventh != '':
      current_scale = ""
  else:
    current_seventh = ""

  text_surface = font.render(current_word + ' ' + current_scale + current_seventh+ ' ' + current_inversion, True, YELLOW)
  text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
  screen.fill(BLACK)
  screen.blit(text_surface,(text_rect[0],20))
  for box in boxes:
    box.render_checkbox()
  pygame.display.flip()



# Function to display the active notes on the screen
def display_notes(notes_string,chord_string):
  text_surface = font.render(notes_string, True, WHITE)
  text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
  background = pygame.draw.rect(screen, BLACK, (0, text_rect[1], screen_width,100 ))
  #screen.fill(BLACK)
  screen.blit(text_surface, text_rect)
  text_surface = small_font.render(chord_string, True, RED)
  background2 = pygame.draw.rect(screen, BLACK, (0,220, screen_width, 220))
  screen.blit(text_surface, (40, 220))
  pygame.display.flip()

def render_checkboxes():
  for box in boxes:
    box.render_checkbox()

  pygame.display.flip()

def midi_notes_to_chord(midi_notes):
  """
  Converts a list of MIDI note numbers to a chord name using music21.

  Args:
      midi_notes: A list of integers representing MIDI note numbers.

  Returns:
      A string representing the chord name, or None if the conversion is not possible.
  """
  if len(midi_notes) > 2:
    # Create a music21 chord object from the notes
    chord_obj = chord.Chord(midi_notes)
    root_note = chord_obj.root().name #WithOctave
    # replace - with b
    root_note = root_note.replace('-','b')
    chord_quality = chord_obj.quality
    name = chord_obj.commonName
    if name == 'dominant seventh chord':
      name = '7'
    if name == 'major seventh chord':
      name = 'Maj7'
    if name == 'minor seventh chord':
        name = 'min7'
    if name == 'major triad':
      name = ' Maj'
    if name == 'minor triad':
      name = ' min'
    if name == 'diminished triad':
      name = 'dim'
    if name[:10] == 'incomplete':
      name = ' unknown'
    inversion_text = chord_obj.inversionText()
    if inversion_text == "Root Position":
      inversion_text = ''
    if inversion_text == "First Inversion":
      inversion_text = '1st'
    if inversion_text == "Second Inversion":
      inversion_text = '2nd'
    chord_name = f"{root_note}{name} {inversion_text}"
    return chord_name
  else:
    return ""


# Display the initial word
display_word()
render_checkboxes()

# Run the main loop
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    # Display a new word on any key press
    elif event.type == pygame.KEYDOWN:
      display_word()
    # checkboxes
    elif  event.type == pygame.MOUSEBUTTONUP:
      for box in boxes:
        box.update_checkbox(event)

      render_checkboxes()
      if boxes[0].checked:
        show_major = True
      else:
        show_major = False

      if boxes[1].checked:
        show_minor = True
      else:
        show_minor = False

      if boxes[2].checked:
        show_accidentals = True
      else:
        show_accidentals = False

      if boxes[3].checked:
        show_inversions = True
      else:
        show_inversions = False

      if boxes[4].checked:
        show_7ths = True
      else:
        show_7ths = False

  # Check for MIDI events (might not be reliable)
  if midi_enabled:
    for msg in inport.iter_pending():
      newNote = True
      if msg.type == 'note_on':
        if msg.velocity:
          # add note to active list
          # if note number is not already in the list
          if msg.note not in active_notes:
            active_notes.append(msg.note)
        else:
          # remove note to active list
          if msg.note in active_notes:
            active_notes.remove(msg.note)
      if msg.type == 'note_off':
        newNote = True
        # remove note to active list
        if msg.note in active_notes:
          active_notes.remove(msg.note)

  if newNote:
    #print(active_notes)
    if midi_enabled:
      display_chord(active_notes)
      chord_string = midi_notes_to_chord(active_notes)
      #if len(chord_string):
        #print(chord_string)
      newNote = False
    if len(active_notes) == 0:
      display_word()

# Quit Pygame
inport.close()
pygame.quit()
