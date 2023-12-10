# Compile All to `.pyc`, Not a secure way to obfuscate your python project


This is not a secure way to obfuscate your code,
but if you don't want people with mid level programming knowledge sniffing around your python project source code then this is a good solution


## Why does it exist?

Each time I want to deploy my whole django project on server I'm worried that my colleagues with access to server can view the source code which they shouldn't, I'm the backend developer for god's sake!

## What does it do?
It compiles your whole python project into `.pyc` files, and you can use them instead of the original source code.


## Requirements:

NOTHING,

it doesn't use any external library