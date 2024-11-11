import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER, ROW

def build(app):
    # Main container box
    main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))

    # Elements: button and input
    button = toga.Button('Submit', on_press=None)
    input = toga.TextInput()
    
    main_box.add(input)
    main_box.add(button)

    def show_new_box(widget):
        # Create a new box with updated content and style
        new_box = toga.Box(style=Pack(direction=ROW, background_color="#00FF00"))
        
        # Label to show the input's content
        input_label = toga.Label(f"Input: {input.value}", style=Pack(padding=5))
        button_delete = toga.Button('Delete', on_press=lambda widget: main_box.remove(new_box))
        
        # Add the label to the new box
        new_box.add(input_label)
        new_box.add(button_delete)
        
        # Add the new box to the main container
        main_box.add(new_box)
        main_box.refresh()  # Refresh layout to display the new box

    # Set button action to show new box
    button.on_press = show_new_box

    return main_box

if __name__ == '__main__':
    app = toga.App('Dynamic Box Example', 'org.beeware.dynamicbox', startup=build)
    app.main_loop()
