# splitmailbox
Simple tool to split your mailbox.

You can customize the directory, prefix, name and suffix of the output mailboxes using the headers of the messages stored in your mailbox. Prefix, name and suffix are expanded by `str.format` function.

## Path of output mailboxes
Prefix, name and suffix are expanded by `str.format` function. The keyword arguments of the function are the header of the mail (see Python class `email.message.Message`), with some extensions:

- `Date` header is a `datetime.datetime` object

## Examples

### Split messages by year
    splitmailbox --suffix '_{Date:%Y}' mail/mbox

Will create the mailboxes `mail/mbox_2000`, `mail/mbox_2001`, ...

## Limitations

- `mbox` format only is supported
- Directory are not created at runtime (e.g. `--prefix '{Date:%Y}/{Date:%m}'`)
