briefs-caster
=============

What is it?
-----------

`Rob Rhyne <http://robrhyne.com/>`_ developed Briefs, an iPhone application for creating wireframes for
Cocoa touch applications.

This is an insanely cool app, and much props go to `Digital Arch
<http://digitalarch.com>`_.

So check it out first, http://getabrief.com.  Ignore briefs-caster if you don't
fall in sappy love with Briefs, this will do you no good.

At some point, while going through the documentation, you will `see some XML
<http://giveabrief.com/docs/share.html>`_.  I
want to warn you about this, because no one warned me and I still have that bile
taste in my mouth from the shock of it.  This XML is used in constructing a
Briefcast.

Briefcasts and briefs-caster
----------------------------

Within Briefs, you can add a URL that points to a list of briefs.  In the app,
it's called **My Briefcasts**.

briefs-caster serves up any ``.brieflist`` file it
finds in a directory you specify and can be entered into the Briefcasts section.

Installation
------------

briefs-caster uses Python.  To install it open a terminal and type the following

::

    easy_install briefs-caster

If you use Pip (recommended), alternatively run this ::

    pip install briefs-caster

*Note* you may need to ``sudo`` these commands on your system.

Usage
-----

We're going to assume that you've installed Briefs and have started using it.
You should be to the point that you have a ``*.brieflist`` file that you've
created by first using the ``bs`` script and then the ``compact-briefs`` script.

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

#. Touch **Briefs-caster example** cell

If everything went as expected, you should see your list of Briefs.
