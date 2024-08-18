# Postmortem

On the release of ALX’s System Engineering & DevOps project (0x19) at approximately 00:07 West Africa Time (WAT), an isolated Ubuntu 20.0  container running an Apache web server experienced an outage. The server returned `500 Internal Server Error` responses for GET requests that were expected to return a simple HTML page displaying a WordPress site.

## Debugging Process

The issue was discovered by our developer, [Your Initials], at around 19:20 WAT when tasked with addressing the problem. The following steps outline the debugging process:

1. Verified running processes using `ps aux`. Two `apache2` processes—`root` and `www-data`—were correctly running.

2. Checked the `sites-available` folder under `/etc/apache2/` to confirm that the web server was serving content from `/var/www/html/`.

3. Initiated `strace` on the PID of the `root` Apache process while making a `curl` request to the server. Unfortunately, this did not reveal any helpful information.

4. Repeated the `strace` process on the PID of the `www-data` Apache process. This time, `strace` returned an `-1 ENOENT (No such file or directory)` error when attempting to access `/var/www/html/wp-includes/class-wp-locale.phpp`.

5. Investigated files within `/var/www/html/` using Vim and pattern matching to locate the erroneous `.phpp` file extension. The typo was found in the `wp-settings.php` file (Line 137: `require_once(ABSPATH . WPINC . '/class-wp-locale.php');`).

6. Corrected the typo by removing the extra trailing `p`.

7. Retested the server with a `curl` request. Success—HTTP 200 OK!

8. Created a Puppet manifest to automate this fix in case the issue recurs.

## Summary

The root cause was a simple typo in the `wp-settings.php` file, where the code referenced `class-wp-locale.phpp` instead of the correct `class-wp-locale.php`. This led to a critical application error preventing WordPress from loading properly.

The patch involved correcting the typo by removing the trailing `p` in the file path.

## Prevention

This outage was an application-level issue rather than a server misconfiguration. To prevent such issues in the future, consider the following measures:

Thorough Testing:** Test applications comprehensively before deployment. This error could have been caught earlier with proper testing.

Monitoring:** Implement uptime-monitoring services (e.g., [UptimeRobot](https://uptimerobot.com/)) to receive instant alerts when the website goes down.

In response to this incident, a Puppet manifest was developed to automatically replace any `.phpp` extensions with `.php` in the `/var/www/html/wp-settings.php` file. This should prevent similar issues from occurring in the future.

Of course, we’re all seasoned developers who never make mistakes, right? 

