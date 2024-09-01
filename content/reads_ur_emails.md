![[tower_banner.png]]

# thing that reads your emails

so i realised a while ago that i am basically incapable of checking my emails...

instead of investing the (like a minute per day tops) effort required to actually look at my emails, i thought "why don't i spend like 17hrs writing an automatic email summarisation bot?"

you can see this project on [github](https://github.com/e74000/reads_ur_emails)

# what it does

`reads_ur_emails` periodically fetches your emails, generates a summary, and sends the summaries to specific discord channels.

# task sheduler

this is really just an openai wrapper strapped to a load of random apis, the only really novel thing in it is the task scheduler library lmao

## how it works

the scheduler takes a set of tasks, each of which can define their own timing rules. currently there are several predefined timing rules for it:

- *once*: runs a task once.
- *every*: runs at a set interval.
- *random*: runs at a random inteval in a set range.
- *daily*: runs daily at a specific time.
- *weekly*: runs on specific days of the week at a set time.
- *monthly*: runs on specific months at a set day and time.

there are also blocking modes that can be used to manage running multiple tasks concurrently

- *non-blocking*: when this task is running, it doesn't prevent any other tasks (or instances of itself) from running.
- *blocking*: only one instance of this (type of) task can run at once, useful for very long lived tasks.
- *global blocking*: no other tasks can run while this task is running.

it supports adding/deleting tasks, error handling including panics and logging (via `slog`)

i thought it was kind of neat so i might make it into its own library at some point. if you want to use it, drop me a dm on twitter and i can move it into its own package.
