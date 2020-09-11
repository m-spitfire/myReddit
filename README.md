# myReddit

This is a project of mine. I inspired by platform Reddit and tried to make a similar platform to it.

## Running locally

For running locally you need to install requirements. To do this run

```cmd
pip install -r requirements.txt
```

Then you need to change some settings to run the server locally. First add some enviroment variables.If you are in windows machine and using a virtual environment you can add them using `set` phrase at the end of _activate.bat_ file:

```bat
rem For running locally you need your `DEBUG` to be `False`
set DEBUG=False
set EMAIL_USER=<the_email_for_sending_reset_password>
set EMAIL_PASSWORD=<password_of_it>

```

If you are not using virtual environment just search up _how to add environment variables?_

If you are using Linux or Mac machine you can run `export` command from terminal:

```bash
$export DEBUG=False
$export EMAIL_USER=<the_email_for_sending_reset_password>
$export EMAIL_PASSWORD=<password_of_it>
```

But if you do not want to use password reset function you do not need to create environment variables related to `EMAIL`.

After installing all the requirements and setting environment variables move to (`cd` into) the project folder _myReddit_ (using `cd myReddit` from command line) and run

```shell
python manage.py runserver
```

Then you are done! Enjoy the site! If you want to contribute anything just fork the repository and create a pull request. Feel free to do that!
