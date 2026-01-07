from matplotlib.patches import Rectangle
from matplotlib.widgets import RectangleSelector
import seaborn as sns
import matplotlib.pyplot as plt
import os
from PIL import Image


def generate_heat_map(layout, full_screen_function, defect_list, df_hue,
                      line_select_callback, company_name, pipe_id, figure):
    print(defect_list)
    print(df_hue)
    # return
    """"
    Generate heap map is a function that will generate Heat map using following params
        :param layout : Layout object in which graph is going to display
        :param full_screen_function : A method that will remove list and make chart visible to full screen
        :param defect_list : List of Defect
        :param df_hue : Data frame to show Heat-map
        :param line_select_callback : A method that will call after every rectangle selection
        :param company_name : A String that will contain Company name
        :param pipe_id : Current Pipe ID
        :param figure : Figure a object of canvas
    """
    plt.clf()
    ax = figure.add_subplot(111)
    rs = RectangleSelector(ax, line_select_callback,
                           drawtype='box', useblit=True,
                           button=[1, 3],
                           minspanx=5, minspany=5,
                           spancoords='pixels',
                           interactive=True)
    plt.connect('key_press_event', rs)
    full_screen_function()
    draw_rectangle(defect_list, ax)
    ax.figure.subplots_adjust(bottom=None, left=None, top=None, right=None)
    #figure.set_size_inches(13.5, 3)
    heat_map_obj = sns.heatmap(df_hue, cmap='Purples')
    heat_map_obj.set(xlabel="Number of Observation", ylabel="Sensors")
    #plt.plot(index,odd1,oddo2)
    save_as_img(heat_map_obj, company_name, pipe_id)
      # to fix the index overlapping
    plt.tight_layout()
    layout.show()
    #layout1.show()
    #plt.tight_layout()


def draw_rectangle(defect_list, ax):
    """"
    Draw rectangle function will draw rectangle with defect list
        :param defect_list : List of defect that will used to draw rectangle
        :param ax : Object of figure that will contain Chart
    """
    for x in defect_list:
        rect_obj = Rectangle((x[0], x[1]), x[2], x[3], fill=False, edgecolor='red')
        ax.add_patch(rect_obj)


def save_as_img(heat_map_obj, company_name, pipe_id):
    """
    This will save the plotted chat as a image format
        :param heat_map_obj:object of seaborn heatmap
        :param company_name:company name used to create folder
        :param pipe_id:Image of graph will be saved as pipe Id
    """
    print(heat_map_obj)
    print(company_name)
    print(pipe_id)
    figure = heat_map_obj.get_figure()

    img_path = os.getcwd() + '/Charts/' + company_name
    img_name = str(pipe_id) + '.png'
    try:
        os.makedirs(img_path)
    except OSError as error:
        pass
    figure.savefig(img_path + '/' + img_name, dpi=400)
    im = Image.open(img_path + '/' + img_name)
    im1 = im.rotate(360, expand=1)
    im1.save(img_path + '/' + img_name)
    # Setting the points for cropped image
    left = 200
    top = 100
    right = 2400
    bottom = 5000

    im = Image.open(img_path + '/' + img_name)
    #im1 = im.crop((left, top, right, bottom))
    im1.save(img_path + '/' + img_name)
