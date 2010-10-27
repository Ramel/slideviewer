Slideviewer is a module for the Itws CMS (python powered).
It add a slideviewer box for Content or Side bar.
Based on the jQuery plugin called Slideviewer, with small adaptations :
 - Resize the images at configured Slideviewer size;
 - Order the images (Itws offer that);
 - Center vertically, or horizontally the image if larger or taller than the configured size.

Slideviewer
=============
http://www.gcmingati.net/wordpress/wp-content/lab/jquery/imagestrip/imageslide-plugin.html

Requirements
=============

Software    Version  Used by           	Home
----------  -------  ----------------  	--------------------------------------
Python          2.6  itws            	http://www.python.org/
itools       0.61.4  itws            	http://www.hforge.org/itools
ikaaro       0.61.4  itws            	http://www.hforge.org/ikaaro
itws	      1.1.1     	     	http://www.hforge.org/itws

Check the Itools/Ikaaro/Itws requirements.


Install
=============

If you are reading this instructions you probably have already unpacked
the Slideviewer tarball with the command line:

  $ tar xzf slideviewer-X.Y.Z.tar.gz

And changed the working directory this way:

  $ cd slideviewer-X.Y.Z

So now to install the module, you just need to type this:

  $ python setup.py install

Stop/Restart the installed Ikaaro/Itws instance:

  $ icms-stop.py ~/databases/myinstance

Edit the instance configuration file:

  $ vim ~/databases/myinstance/config.conf

Add "slideviewer" to the modules line:

  modules = itws slideviewer

Update database, and catalog, if needed or simply restart the instance:

  $ icms-update.py ~/databases/myinstance

  $ icms-update-catalog.py ~/databases/myinstance

  $ icms-start.py -d ~/databases/myinstance

Now, in an Itws website instance, you should see a new Box type called "Slideviewer".
