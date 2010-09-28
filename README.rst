briefs-caster
=============

What is it?
-----------

This is a simple Briefcasts server for your Briefs.

`Rob Rhyne <http://robrhyne.com/>`_ developed Briefs, an iPhone application for creating wireframes for
Cocoa touch applications.

This is an insanely cool app, and much props go to `Digital Arch
<http://digitalarch.com>`_.  Check it out first, http://giveabrief.com.

Briefcasts and briefs-caster
----------------------------

Within Briefs, you can add a URL that points to a list of briefs.  In the app,
it's called **My Briefcasts**.

briefs-caster converts any ``.bs`` files into ``.brieflist`` files using the
utilities provided by `the Briefs starter kit
<http://giveabrief.com/files/starterkit.zip>`_ and serves them up on
http://0.0.0.0:5000 as a Briefcast.

Installation
------------

*Requires Mac OS X*

briefs-caster uses Python.  To install it open a terminal and type the following

::

    easy_install briefs-caster

If you use Pip (recommended), alternatively run this ::

    pip install briefs-caster

*Note* you may need to ``sudo`` these commands on your system.

Usage
-----

We're going to assume that you've installed Briefs and have started using it.
You should be to the point that you have a ``.bs`` file that you've
created.

Let's pretend it's in a directory called ``~/my_briefs``.

Run the briefs-caster from the directory ::

    cd ~/my_briefs
    briefs-caster

Alternatively you can tell briefs-caster where to serve from ::

    briefs-caster ~/my_briefs

You should see the following output ::

    briefs-caster - Serving up some fine briefs for you

    Open http://<IP_ADDRESS>:5000 from the Briefs app

    CTRL-C to exit the server
    * Running on http://0.0.0.0:5000/

Errors
------

Check the terminal for any errors that the Briefs script utililty produces.  If
you mis-type something, forget a required attribute or something like that it
will show up in the output.


Add to Briefs
-------------

In the Briefs app do the following:

#. Touch **My Briefcasts**
#. Touch **Edit** in the top right
#. Touch **+**
#. Enter Name **Briefs-caster example**
#. Enter URL **http://127.0.0.1:5000** or if you are not using the same computer
   this IP may be different (we run the iPhone Simulator with Briefs inside it)
#. Touch **Save**
#. Touch **Done**

Now you are ready to try it out:

#. Touch **Briefs-caster example**

If everything went as expected, you should see your list of Briefs.
