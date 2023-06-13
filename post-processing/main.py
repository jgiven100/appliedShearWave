import os
import plot


def main():
    """
    save is boolean to save figures
    """
    save = False
    """
    dir_name is directory name where data is currently saved and used for 
    location to save figure
    """
    dir_name = 'compliant/'

    # Set directory name for saving
    saveDir = 'post-processing/figs/' + dir_name

    # Make directory if it does not exist
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)

        # No warning if new directory
        warn = False

    # Set warning if directory already exists
    else:
        warn = True

    # Change current directory to correct location
    os.chdir(saveDir)

    # Warn and quit if new figures will override old figures
    if save and warn:
        print('Warning: plot save location already exists!!')
        quit()

    # Plot
    plot.plot(save, dir_name)


if __name__ == '__main__':
    main()