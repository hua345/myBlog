# manim参数

```bash
$ python -m manim -h
usage: manim.py [-h] [-p] [-w] [-s] [-l] [-m] [--high_quality] [-g] [-i] [-f]
                [-t] [-q] [-a] [-o FILE_NAME] [-n START_AT_ANIMATION_NUMBER]
                [-r RESOLUTION] [-c COLOR] [--sound] [--leave_progress_bars]
                [--media_dir MEDIA_DIR]
                [--video_dir VIDEO_DIR | --video_output_dir VIDEO_OUTPUT_DIR]
                [--tex_dir TEX_DIR]
                file [scene_names [scene_names ...]]

positional arguments:
  file                  path to file holding the python code for the scene
  scene_names           Name of the Scene class you want to see

optional arguments:
  -h, --help            show this help message and exit
  -p, --preview         Automatically open the saved file once its done
  -w, --write_to_movie  Render the scene as a movie file
  -s, --save_last_frame
                        Save the last frame
  -l, --low_quality     Render at a low quality (for faster rendering)
  -m, --medium_quality  Render at a medium quality
  --high_quality        Render at a high quality
  -g, --save_pngs       Save each frame as a png
  -i, --save_as_gif     Save the video as gif
  -f, --show_file_in_finder
                        Show the output file in finder
  -t, --transparent     Render to a movie file with an alpha channel
  -q, --quiet
  -a, --write_all       Write all the scenes from a file
  -o FILE_NAME, --file_name FILE_NAME
                        Specify the name of the output file, ifit should be
                        different from the scene class name
  -n START_AT_ANIMATION_NUMBER, --start_at_animation_number START_AT_ANIMATION_NUMBER
                        Start rendering not from the first animation, butfrom
                        another, specified by its index. If you passin two
                        comma separated values, e.g. "3,6", it will endthe
                        rendering at the second value
  -r RESOLUTION, --resolution RESOLUTION
                        Resolution, passed as "height,width"
  -c COLOR, --color COLOR
                        Background color
  --sound               Play a success/failure sound
  --leave_progress_bars
                        Leave progress bars displayed in terminal
  --media_dir MEDIA_DIR
                        directory to write media
  --video_dir VIDEO_DIR
                        directory to write file tree for video
  --video_output_dir VIDEO_OUTPUT_DIR
                        directory to write video
  --tex_dir TEX_DIR     directory to write tex
```
