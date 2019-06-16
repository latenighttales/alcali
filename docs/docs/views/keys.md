# Keys

![keys](../images/keys.png)
If you use Alcali master returner, Keys should be automatically refreshed. That's the only difference from the original [MySQL Salt returner](https://docs.saltstack.com/en/latest/ref/returners/all/salt.returners.mysql.html).

Otherwise, you should refresh keys manually using the _fab_ button.

!!!danger "Action buttons"

    To make life easier, states used to manage keys are more radical than default salt behaviour.
    
    It means that if you use the **`REJECT`** button, it will use `include_accepted` and `include_denied` argument.
    
    If you use the **`ACCEPT`** button, it will use `include_rejected` and `include_denied` argument.
    
    Use wisely.
