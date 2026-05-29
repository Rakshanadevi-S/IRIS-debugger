// utils/examples.js
// Pre-built Python error examples to quickly populate the input

const EXAMPLES = {
  KeyError: `Traceback (most recent call last):
  File "app.py", line 5, in <module>
    print(user['email'])
KeyError: 'email'`,

  TypeError: `Traceback (most recent call last):
  File "calc.py", line 3, in <module>
    result = "Total: " + 42
TypeError: can only concatenate str (not "int") to str`,

  NameError: `Traceback (most recent call last):
  File "script.py", line 7, in <module>
    send_email(mesage)
NameError: name 'mesage' is not defined`,

  IndexError: `Traceback (most recent call last):
  File "main.py", line 4, in <module>
    print(items[5])
  File "main.py", line 4, in <module>
IndexError: list index out of range`,

  AttributeError: `Traceback (most recent call last):
  File "process.py", line 9, in <module>
    data.sort()
AttributeError: 'NoneType' object has no attribute 'sort'`
};
