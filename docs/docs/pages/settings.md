# Settings

## General Settings

### Parse modules

To provide function completion and documentation run this on a selected target.

This will run `sys.list_functions`, `sys.doc`, `sys.list_runner_functions` and `sys.runner_doc` on the selected target. 

It will also run `doc.wheel` on the connected salt master.

If you have custom modules present on the selected target, they will be parsed too.

### Minions Fields

To add more details in the [minion detail](minion_details.md) page, you can add custom minions fields.

We usually add:

 - **highstate**: `state.show_highstate`
 - **top file**: `state.show_highstate`
 
!!!info
    
    Because minions fields are linked to minions, you need to first have some minions present in the database.
    
    Use the [refresh minions](minions.md) button.
    
## User Settings

### Job notifications

Filter which events are being displayed in the notification section and real-time events.

!!!warning
    Salt's event stream is **very** busy and can easily overwhelm the available memory for a browser tab.
    This control both notifications and [real-time events](overview.md#real-time-events) on the overview page.
