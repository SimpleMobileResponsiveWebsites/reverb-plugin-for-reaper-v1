Reverb plugin for Reaper

Step 1: Set up Reaper for JSFX Scripting

Open Reaper.

Go to Options > Show REAPER resource path in explorer/finder.

Open the Effects folder.

Create a new folder for your effects if you like, and create a new file with the extension .jsfx (e.g., SimpleReverb.jsfx).

Step 2: Create the Basic Structure of the Plugin
Paste the following code into your .jsfx file. This code will implement a basic reverb with controls for room size, damping, and mix (wet/dry) balance.


Creating a reverb plugin for Reaper requires using the JSFX (Jesusonic FX) scripting language. Reaper's built-in scripting allows us to write custom audio effects that can be used directly in Reaper. Here, I’ll walk you through a simple example of a reverb plugin that you can customize.

This script will apply a simple delay-based reverb, sometimes called a “schroeder reverb.” More advanced reverb effects, such as convolution reverb, would require more complex algorithms and processing.

Step 1: Set up Reaper for JSFX Scripting
Open Reaper.
Go to Options > Show REAPER resource path in explorer/finder.
Open the Effects folder.
Create a new folder for your effects if you like, and create a new file with the extension .jsfx (e.g., SimpleReverb.jsfx).
Step 2: Create the Basic Structure of the Plugin
Paste the following code into your .jsfx file. This code will implement a basic reverb with controls for room size, damping, and mix (wet/dry) balance.



desc: Simple Reverb
// Tags: reverb, delay
// A simple reverb plugin for Reaper using delay lines for reverb effect.

// @init section: initialize variables
@init
// Default parameter values
room_size = 0.5;
damping = 0.5;
mix = 0.3;

// Delay buffer sizes
max_delay_samples = 44100; // Max delay of ~1 second for 44100 Hz sample rate
delay_bufferL = 0;
delay_bufferR = 0;
delay_index = 0;

// Initialize delay buffers
delay_bufferL = max_delay_samples;
delay_bufferR = max_delay_samples;
loop(44100, delay_bufferL[0] = delay_bufferR[0] = 0;); // Clear buffers

// @slider section: user-adjustable parameters
slider1:Room Size=0.5<0,1,0.01> // Room size, affects delay length
slider2:Damping=0.5<0,1,0.01> // Damping, controls feedback level
slider3:Mix=0.3<0,1,0.01> // Wet/Dry Mix

// @sample section: per-sample processing
@sample
// Convert sliders to local variables
room_size = slider1;
damping = slider2;
mix = slider3;

// Calculate delay length based on room size
delay_samples = max_delay_samples * room_size;

// Process left and right channels separately
inL = spl0;
inR = spl1;

// Get delayed samples
outL = delay_bufferL[delay_index];
outR = delay_bufferR[delay_index];

// Write input samples to the delay buffer with feedback
delay_bufferL[delay_index] = inL + damping * outL;
delay_bufferR[delay_index] = inR + damping * outR;

// Update delay buffer index
delay_index += 1;
delay_index %= delay_samples;

// Mix dry and wet signals
spl0 = (1 - mix) * inL + mix * outL;
spl1 = (1 - mix) * inR + mix * outR;
Explanation of the Code
@init Section: This is where we set up constants and variables that we will use throughout the plugin. We define the max_delay_samples for our delay buffer, initialize empty delay buffers, and define the plugin's parameters (room size, damping, and mix).

@slider Section: Defines the sliders, which appear as user controls in Reaper. Each slider corresponds to a specific parameter:

Room Size affects the delay length.
Damping affects the feedback level in the delay loop.
Mix is the wet/dry balance between the original and reverb-processed signals.
@sample Section: The main processing loop that runs for every audio sample:

First, we calculate the delay length (delay_samples) based on the room size.
Then, we retrieve the delayed samples (outL and outR).
We add the current input samples to the delay buffers with feedback (damping).
We update the delay buffer index and wrap it back to zero once it reaches the delay length (delay_samples).
Finally, we output a mix of the dry and wet signals based on the mix slider setting.
Additional Customization Tips
Add More Delay Lines: Increasing the number of delay lines can give a more complex, natural reverb sound.
Modulate Delay Times: Adding slight modulation to delay times can create a “chorused” reverb effect.
Include High-Pass and Low-Pass Filtering: Add a simple filter to the feedback loop to remove low frequencies or attenuate high frequencies, which can make the reverb sound more natural.
Using the Reverb in Reaper
After saving your .jsfx file, open Reaper and insert the effect on a track.
Go to FX > Add FX > JS and look for your script by name (e.g., SimpleReverb).
Adjust the sliders to test out the effect. The Room Size and Damping sliders should give you a variety of reverb sounds, while the Mix slider blends between the dry and wet signals.


Writing The Graphical User Interphase To The Plugin

Reaper’s JSFX does support basic graphical UI elements, although it's somewhat limited. We can create a basic graphical interface with visual elements like sliders, meters, and labels for our reverb plugin. Here’s how to enhance the plugin with a simple UI in the JSFX scripting language.

Step 1: Set Up Basic Graphics Variables
To add a GUI, we need to add a section called @gfx, which is used for rendering the graphical interface. Reaper provides some basic drawing functions in JSFX, like gfx_rect, gfx_line, and gfx_text, which we can use to create our UI.

Add this code below the previous script. This will add custom-drawn sliders and labels for Room Size, Damping, and Mix.

Explanation of the GUI Code

@gfx Section: This is where all the GUI drawing and interaction logic is implemented. Here’s a breakdown of the main sections:

Slider Display: Each slider has a position and size on the screen, and it’s drawn as a filled rectangle. The length of each rectangle (the width in this case) reflects the current slider value.
Text Labels: Each slider is labeled with its name and the current value. Text is drawn with the gfx_printf function.
Mouse Interaction: The handle_slider function checks if the mouse is over a slider and then updates the slider value based on the mouse’s X position when clicked. This allows you to click and drag the slider for real-time control.
Mouse Control for Sliders: Each slider has an interactive region. When you click and drag within this region, the handle_slider function calculates the new value for each slider based on the X position of the mouse.

Color and Fonts: Colors are set with gfx_r, gfx_g, gfx_b for RGB values and gfx_a for opacity. You can change these values to customize the appearance. The gfx_setfont function sets up the font style and size for the labels.

Using and Testing the Plugin
Save the updated .jsfx file and reload it in Reaper.
Adjust the sliders by clicking and dragging over the graphical sliders you created.
The sliders should now affect the Room Size, Damping, and Mix parameters in real-time.
This setup provides a basic but functional GUI for the reverb effect. The simplicity of JSFX’s drawing tools limits the design somewhat, but you can use additional graphical functions, like gfx_line, gfx_circle, and others, for more complex interfaces.



Here are the key features Of the Rossow Reverb LiquidSonic:

Controls:


Size: Controls the room size of the reverb
Predelay: Adds initial delay before the reverb
Chorus: Adds modulation to the reverb tail
Width: Controls the stereo width
Decay: Controls how long the reverb tail lasts
Output: Controls the output level (-12dB to +12dB)
Dry/Wet: Controls the mix between dry and wet signal


GUI Features:


Professional dark theme matching the reference image
Knob-based controls with value displays
VU meter for output monitoring
Clean, organized layout
Smooth parameter control


DSP Features:


High-quality stereo reverb algorithm
Modulation section for chorus effects
Width control for stereo image adjustment
Predelay buffer for initial delay
Smooth parameter interpolation

To use this plugin in REAPER:

Copy the code into a new JSFX effect
Save it in your REAPER Effects folder
Load it on any track or send
  


