# Importing requirements.
import pytube # Python library for downloading YouTube videos.
import customtkinter as cs # Main module for designing GUI.
from tkinter import * 
from tkinter import messagebox # For displaying important messages
from PIL import Image # Displaying images for customtkinter
import urllib.request # For dowmloading images from the web.

# Start to code here.
cs.set_appearance_mode("system")
cs.set_default_color_theme('dark-blue')

# Define the main window
main = cs.CTk(fg_color=("#CFCFCF"))
main.title("Music media player")
main.geometry("400x440")
main.resizable(False, False)

def search():
    """Function for searching using link user inputed."""

    global youtube_vid

    try:
        url = search_box.get() # Get the user input
        youtube_vid = pytube.YouTube(url) # Search for the YT video

        # Displaying the title the thumbnail.
        thumb_url = youtube_vid.thumbnail_url
        display_thumbnail(thumb_url)

        # Displaying the title.
        title = youtube_vid.title # Get YT video title.
        display_title(title)

        # Displaying the video resolution.
        display_vid_res(youtube_vid)

        # Displaying the audio resolution.
        display_aud_res(youtube_vid)
        
    # Exception if the link is not valid.
    except pytube.exceptions.RegexMatchError:
        reset_defult()
        messagebox.showerror("Invalid URL", "Please enter a valid YouTube video URL.")

    # Exception if the video is age restricted.
    except pytube.exceptions.AgeRestrictedError:
        reset_defult()
        messagebox.showerror("Age Restriction", "Video is not available for your age.") 

    # Exception if the video is members only.
    except pytube.exceptions.MembersOnly:
        reset_defult()
        messagebox.showerror("Members Only", "This video is for members only.") 

    # Exception if reading of the video is incomplete.
    except pytube.exceptions.IncompleteRead:
        reset_defult()
        messagebox.showerror("Read Incomplete", "Video reading is incomplete click search AGAIN.")

    # Exception if the video is a live stream.
    except pytube.exceptions.LiveStreamError:
        reset_defult()
        messagebox.showerror("Live Stream", "Live stream can not be downloaded.")


def video_dl():
    """Function for downloading the video."""
    
    # Get the YouTube instance.
    global youtube_vid
    video = youtube_vid 

    if video != '': # If the YouTube instance is not defult.
        # Getting the selected resolution to download. 
        selected_res = v_combo_var.get().strip()

        # Filtering the streams to download the specified specs. 
        stream = video.streams.filter(res=selected_res).first()

        if selected_res != '': # If the combobox is not defult.
            stream.download(output_path='downloaded_files/videos') # Download method of pytube instance.
        else: # If the combobox is not defult.
            return
    else: # If the YouTube instance is defult.
        return


def audio_dl():
    """Function for downloading the audio."""

    # Get the YouTube instance.
    global youtube_vid
    video = youtube_vid

    if video != '': # If the YouTube instance is not defult.
        # Getting the selected kbps to download. 
        selected_res = a_combo_var.get().strip()
        
        # Filtering the streams to download the specified specs.
        stream = video.streams.filter(abr=selected_res).first()

        if selected_res != '': # If the combobox is not defult.
            stream.download(output_path='downloaded_files/audios', filename=f'{video.title}.mp3')
        else: # If the combobox is not defult.
            return
    else: # If the YouTube instance is defult
        return
    

def get_video_res(video):
    """Return list of the YouTube video resolution."""

    # Resolutoin container.
    res_list = []

    # Loop through all the video streams that can be downloaded. 
    for stream in video.streams.filter(only_video=True): 
        #Get the resolution and turn it into int.
        res = int(stream.resolution.replace('p', ''))
        
        if res not in res_list: # Check if the resolution is already in the container.
            res_list.append(res) # If not add it to the list.
    
    # Store the sorted resolutions and turned it back to the str.
    resolution_list = [str(res)+'p' for res in sorted(res_list, reverse=True)]

    return resolution_list # Return the sorted list of resolutions.


def get_audio_res(video):
    """Return list of the YouTube audio resolution."""

    # Kbps container.
    abr_list = []

    # Loop through all the audio streams that can be downloaded. 
    for stream in video.streams.filter(only_audio=True):
        #Get the kbps and turn it into int.
        abr = int(stream.abr.replace('kbps', ''))
        
        if abr not in abr_list: # Check if the abr is already in the container.
            abr_list.append(abr) # If not add it to the list.
    
    # Store the sorted kbps and turned it back to the str.
    abr_list_sorted = [str(abr)+'kbps' for abr in sorted(abr_list, reverse=True)]

    return abr_list_sorted # Return the sorted list of abr.

 
def display_vid_res(video):
    """Displaying the resolution for the selected YouTube video that can be downloaded."""

    # Get the sorted resulotions.
    resolutions = get_video_res(video)

    # Set the values of the combobox to the resolutions.
    v_res_combo.configure(state="readonly")
    v_res_combo.configure(values=resolutions)
    v_res_combo.set(resolutions[0])


def display_aud_res(video):
    """Displaying the resolution for the selected YouTube video that can be downloaded as audio."""

    # Get the sorted kbps.
    abr = get_audio_res(video)

    # Set the values of the combobox to the kbps.
    a_res_combo.configure(state="readonly")
    a_res_combo.configure(values=abr)
    a_res_combo.set(abr[0])


def display_thumbnail(thumbnail_url):
    """For displaying the YouTube thumbnail."""

    # Downloading the thumbnail internally.
    urllib.request.urlretrieve(thumbnail_url, "images/thumbnail.png")
    # Create a CTkImage instance.
    thumbnail_img = cs.CTkImage(dark_image=Image.open("images/thumbnail.png"), size=(376, 200))
    # Remove the text inside the thumbnail containter 
    thumbnail.configure(text='')
    # Display the downloaded thumbnail.
    thumbnail.configure(image=thumbnail_img)
    

def display_title(title):
    """For displaying the YouTube title."""

    # Displaying the title of the YT video.
    yt_title.delete(0, END)
    yt_title.insert(END, title)


def reset_defult():
    """For setting back all to defult."""

    global youtube_vid
    # Setting back the YouTube object as empthy str.
    youtube_vid = ''

    # Setting the thumbnail label back to defult.
    thumbnail.configure(text='Thumbnail here.')
    thumbnail.configure(image=defult_thumbnail)

    # Setting the title label back to defult.
    yt_title.delete(0, END)
    yt_title.insert(END, "YouTube video title here.")

    # Setting the combobox back to defult.
    # Video
    resolutions = []
    v_res_combo.set('')
    v_res_combo.configure(values=resolutions)
    v_res_combo.configure(state="disabled")
    # Audio
    abr = []
    a_res_combo.set('')
    a_res_combo.configure(values=abr)
    a_res_combo.configure(state="disabled")


# Defining youtube_vid object as global.
global youtube_vid
youtube_vid = ''
# Defining necessary colors and font style for styling.
font_color = "#0E0101"
font_name = "Bahnschrift"
main_bg_clr = "#CFCFCF"
brand_clr = "#BB2B2B"
hover_clr = "#B7B7B7"
# Definfg the image for btn.
search_btn_img = PhotoImage(file="images/search-btn.png")
dl_btn_img = PhotoImage(file="images/download-btn.png")
# Defining the thumbnail background 'defult'.
defult_thumbnail = cs.CTkImage(dark_image=Image.open("images/thumbnail-bg.png"), size=(376, 200))


# Defining the main frame.
main_frame = cs.CTkFrame(main, fg_color="transparent")
main_frame.pack(expand=True, fill=BOTH, padx=12, pady=12)


# Search frame.
search_main_frame = cs.CTkFrame(main_frame, fg_color="transparent")
search_main_frame.pack(fill=X, pady=(0, 8)) 
# Search box.
search_box = cs.CTkEntry(
    search_main_frame, 
    placeholder_text="Enter Youtube link here.",
    height=40, 
    text_color=font_color, 
    font=(font_name, 14),
    fg_color=main_bg_clr, 
    corner_radius=6, 
    placeholder_text_color="#737373",
    border_color=brand_clr,
)
search_box.pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
# Search button in the right side.
search_btn = Button(
    search_main_frame, 
    image=search_btn_img, 
    borderwidth=0,
    bg=main_bg_clr, 
    activebackground=main_bg_clr,
    command=search
)
search_btn.pack(side=LEFT)


# Result frame for title and thumbnail.
result_main_frame = cs.CTkFrame(main_frame, fg_color="transparent")
result_main_frame.pack(fill=X) 
# Frame for the thumbnail.
thumbnail_frame = cs.CTkFrame(result_main_frame, fg_color='transparent')
thumbnail_frame.pack()
# Thumnail label that will contain the thumbnail image of the YT video.
thumbnail = cs.CTkLabel(
    thumbnail_frame, 
    text='Thumbnail here.',
    text_color=font_color,
    font=(font_name, 16, 'bold'),
    height=200,
    image=defult_thumbnail
)
thumbnail.pack()
# Title text
yt_title = Listbox(
    result_main_frame,
    bg=main_bg_clr,
    fg=font_color,
    font=(font_name, 12, "bold"),
    width=24,
    height=1,
    borderwidth=0,
    highlightthickness=0,
    activestyle="none",
    relief=FLAT,
    selectbackground=main_bg_clr,
    selectforeground=font_color, 
    justify=CENTER
)
yt_title.pack(fill=X, pady=(8, 8))
yt_title.insert(END, "YouTube video title here.")


# Main frame for the download part.
specs_main_frame = cs.CTkFrame(main_frame, fg_color="transparent")
specs_main_frame.pack(fill=X) 
# Frame for the mp4 file type download.
v_lb_frame = cs.CTkFrame(specs_main_frame, fg_color="transparent")
v_lb_frame.pack(fill=X)
# mp4 file type label.
video_label = cs.CTkLabel(
    v_lb_frame, 
    text="MP4 (video)", 
    font=(font_name, 12, 'bold'),
    anchor="w", 
    text_color=font_color
)
video_label.pack(fill=BOTH, padx=4)
# Frame for the resolution combobox.
v_spec_frame = cs.CTkFrame(specs_main_frame, fg_color="transparent")
v_spec_frame.pack(fill=X, pady=(0, 12))
# Variable for the resolution combobox.
v_combo_var = cs.StringVar()
# Resolution combobox.
v_res_combo = cs.CTkComboBox(
    v_spec_frame, 
    width=200, 
    fg_color=main_bg_clr, 
    border_color=brand_clr, 
    button_color=brand_clr, 
    border_width=2, 
    height=32, 
    dropdown_fg_color=main_bg_clr, 
    dropdown_hover_color=hover_clr,
    dropdown_text_color=font_color, 
    dropdown_font=(font_name, 12),
    state="disabled", 
    text_color=font_color, 
    font=(font_name, 12),
    variable=v_combo_var
)
v_res_combo.pack(side=LEFT, padx=(0, 8), fill=X, expand=True)
# mp4 file type download btn.
v_dl_btn = Button(
    v_spec_frame, 
    text='', 
    image=dl_btn_img, 
    borderwidth=0,
    bg=main_bg_clr, 
    activebackground=main_bg_clr,
    command=video_dl
)
v_dl_btn.pack(side=LEFT)

# Mian frame for the mp3 file type download.
audio_frame = cs.CTkFrame(specs_main_frame, fg_color="transparent")
audio_frame.pack(fill=X)
# Frame for the mp3 file type download.
a_lb_frame = cs.CTkFrame(audio_frame, fg_color="transparent")
a_lb_frame.pack(fill=X)
# mp3 file type label.
audio_label = cs.CTkLabel(
    a_lb_frame, 
    text="MP3 (audio)", 
    font=(font_name, 12, 'bold'),
    anchor="w", 
    text_color=font_color
)
audio_label.pack(fill=BOTH, padx=4)
# Variable for the Kbps combobox
a_combo_var = cs.StringVar()
# Kbps esolution combobox
a_res_combo = cs.CTkComboBox(
    audio_frame,
    width=200, 
    fg_color=main_bg_clr, 
    border_color=brand_clr, 
    button_color=brand_clr, 
    border_width=2, 
    height=32, 
    dropdown_fg_color=main_bg_clr, 
    dropdown_hover_color=hover_clr,
    dropdown_text_color=font_color, 
    dropdown_font=(font_name, 12), 
    state="disabled", 
    text_color=font_color,                           
    font=(font_name, 12),
    variable=a_combo_var
)
a_res_combo.pack(side=LEFT, padx=(0, 8), fill=X, expand=True)
# mp4 file type download btn.
a_dl_btn = Button(
    audio_frame, 
    text='', 
    image=dl_btn_img, 
    borderwidth=0,
    bg=main_bg_clr, 
    activebackground=main_bg_clr,
    command=audio_dl,
)
a_dl_btn.pack(side=LEFT)

# Main loop of the GUI.
main.mainloop()
