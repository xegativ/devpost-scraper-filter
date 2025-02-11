from flask import Flask, render_template, request, redirect, session
import os

import logging
from dps import DPS


def create_app():
    logging.basicConfig(level=logging.DEBUG)

    # name of current python module
    # used to tell the instance where it is located
    app = Flask(__name__)

    app.secret_key = os.urandom(24)

    # decorator
    # render_template() utilizes Jinja template engine
    # we can either use decorator or app.add_url_rule('/','hello',function)
    @app.route("/", methods=("GET", "POST"))
    def index():
        app.logger.info("> Index page called")
        # init
        # Initialize URL_lst in the session

        # app.logger.info(f'> SESSION BEFORE CHECK: {session["URL_lst"]}!')

        if "URL_lst" not in session:
            session["URL_lst"] = []
            session.modified = True
        if "URL_data" not in session:
            session["URL_data"] = []
            session.modified = True

        app.logger.info(f'> SESSION AFTER CHECK: {session["URL_lst"]}!')

        URL_lst = session["URL_lst"]
        URL_data = session["URL_data"]
        return render_template("index.html", URL_lst=URL_lst, URL_data=URL_data)

    @app.route("/add", methods=("GET", "POST"))
    def add():
        if "ADD" in request.form:
            app.logger.info("> Add page called")
            if "URL" in request.form:
                URL = request.form["URL"].strip()

                app.logger.info(f"> URL: {URL}")

                # if exists and not in session, add to session list
                if URL and URL not in session["URL_lst"]:
                    session["URL_lst"].append(URL)
                    session.modified = True

                    app.logger.info(f"> UNIQUE URL!")
                    app.logger.info(f'> SESSION AFTER ADD: {session["URL_lst"]}!')
        elif "GETDATA" in request.form:
            if "n_subm" in request.form:
                try:
                    n_subm = int(request.form["n_subm"])
                except:
                    n_subm = 0
            else:
                n_subm = 0
            app.logger.info(f"> N_SUBM={n_subm}")

            if "n_page" in request.form:
                try:
                    n_page = int(request.form["n_page"])
                except:
                    n_page = 0
            else:
                n_page = 0
            app.logger.info(f"> N_SUBM={n_page}")

            if "DontCheckWinner" in request.form:
                DontCheckWinner = not request.form["DontCheckWinner"]
            else:
                DontCheckWinner = True

            URL_DATA_OBJ = DPS(session["URL_lst"], n_subm, n_page, DontCheckWinner)
            URL_get_data = URL_DATA_OBJ.getData()
            app.logger.info(f"> DATA: {URL_get_data}")

            # not appending
            # as it is changing completely
            session["URL_data"] = URL_get_data
            session.modified = True
        else:
            pass

        return redirect("/")

    @app.route("/delete", methods=("GET", "POST"))
    def delete():
        app.logger.info("Delete page called")
        i = int(request.form["INDEX"])

        session["URL_lst"].pop(i)
        session.modified = True

        return redirect("/")

    return app


# if __name__ == "__main__":
#     app.run(debug=True)
