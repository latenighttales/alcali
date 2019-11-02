# Upgrade

!!!danger

    **Each time you upgrade Alcali, you must apply database migrations.**

To do so, you must first stop the service, upgrade, and then, just run:

```bash
alcali migrate
```

And restart the service.
