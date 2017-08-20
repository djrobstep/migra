With migra you can dispense with schema version numbers and multiple migration files.

## Different deployment styles

Migra doesn't force a precise workflow onto you, because every project is different. Instead, migra was designed to allow you to easily script up the workflow you want, help you automate it as fast as possible, and help you test your database changes to ensure correctness.

Nevertheless, here's some guidelines about how set things up just right.

### App-driven vs database-driven

Broadly speaking there are two ways to manage changes to an application database, which we might call app-centric and database-centric. You can use `migra` to enhance either style, however you'll use it quite differently depending on your preferred situation.

With the app-centric approach, you add migration files to the same repository as your application code. When you deploy, any new migration files that haven't yet been applied to the production database get run before the app code is deployed.

The database-centric approach is more common in an environment where you have separate people responsible for the database. Sysadmins or DBAs manage database changes as a separate task. App and DB deployments are more loosely coordinated and not run at the same time as part of the same deployment.

The key feature of both is to directly use the production schema generate the changes needed.

### Migra with app-driven deployments

Instead of manually crafting migration files and mucking about with version numbers, you can do the following.

- dump the schema of your production database
- use migra to generate the changes required to move your production database to the new intended state. edit this script as necessary and add it to source control
- write tests to ensure that your app works after the migration has been applied and that it results in the exact schema you want
- add a step to your deployment that does a schema comparison to see if any of the scripts you've added to source control need applying. unlike traditional migration tools, no version numbers are needed here because the script checks the structure of the database directly.
- then applies the scripts, tests the schema again to check the script has resulted in the correct structure, then deploys the rest of the app as usual.

### Migra with database-centric deployments

The flow with a database-centric application might look like this:

- dump the production database schema and generate the changes required.
- write tests to ensure correct functioning of the application (both before and after the database changes)
- deploy the application
- subsequently, apply the generated migration script on the production database.
