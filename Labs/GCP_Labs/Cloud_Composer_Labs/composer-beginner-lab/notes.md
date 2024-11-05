great, now I want you to write a function which does the following:

it plots a mechanical property versus a fusion parameter if we pass the mechanical property and fusion parameter as the arguements to the function. it plots it as scatter plots, and also check if there is 'mech_prop_plots' directory in the current directory, if there is it saves the plot in that directory, if there is no, it creates a directory. also saves the plot with an appropriate name. also the x axis and y axis labels should be capitilized and if there is underscore or the unit of the mechanical property in the name, it removes those. 

also no need to have a grid on, also when you plot those, all plots should be the same sizing, and also add a arguements to the function (boolean) which determines if it is True, it plots the dots in red, if not it plots it with black color. also write the function in way which in the function body pass a random font size for x axis and y axis label so I can play with the font size myself. also x axis ticks and y axis ticks pass a random fontsize for those too. the background of the plot should be white, and it should just have the left y axis and bottom x axis.

also below are the list of the mechanical properties, 

'stiffness_tex', 'linearStrength_tex', 'strength_tex',
       'resilience_Jpermg', 'toughness_Jpermg'

and below is the list of fusion parameters

'Frequency', 'Voltage', 'Cycle', 'Time', 'current'

