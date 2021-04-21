# Firm Miner
## About the project
I created this project to showcase my work and modestly contribute to Robin AI's success. I wasn't exactly sure what
to build at first, as there isn't enough information on the website. I thought a client origination software might be
independent of your current stack and useful enough to reach out to new potential clients.
I decided to go after *Top UK Law Firms* as potential clients. Robin AI can be a great addition to these 
companies regarding their contracts generation and verification processes. By automating these processes, the clients 
would be able to reduce their operation costs.
The goal is to collect data about these law firms and the attorneys working there. After applying some filtering 
criteria to find attorneys in certain industries (corporate lawyers for example), a sales person from robin ai would 
then cold email "en masse" in order to pitch robinai's products and bring in new customers.
## Architecture
This project consists of 4 main services. All the services are dockerized and managed using docker compose for 
simplicity.
### Scraper
I built a spider using scrapy that fetches attorney firm data from [legal500.com](https://legal500.com). You can check
some sample data in the output directory, but this is not a full run of the system.
1) This spider would crawl all the main areas of the UK to identify potential law firms operating in these areas.
2) It would then parse each individual firm's page and collect relevant data about these firms (location, 
   email, firm name, areas of practices, etc)
3) If there's data available, we would then scrape the information for all the attorneys working fora that firm. This 
would allow us to send more customized emails and therefore increasing the open and reply rates on these emails.
4) When an attorney is parsed, we are exporting the scraped items (attorney and attorney firms) to different 
   destinations:
   4.1) We export the data as a csv dump to AWS S3 and to be easily analyzed by a human.
   4.2) We export the data as a json dump to AWS S3 and to be integrated or used by other services.
   4.3) I saw that robinai is using AWS SQS. The scraper will also upload the scraped data as JSON format to amazon SQS 
   in case you want to integrate the results into another service. For example, to integrate the output with a service 
   that would insert this data into your CRM.
### Database
We are using a postgres database to keep track of the data and to run the django webapp. We are not doing any volume 
mapping on the db again for testing purposes. This implies that every time the services are restarted we start with a 
fresh database.
### Webapp
The webapp consists of a simple django web application running in docker behind a gunicorn webserver. The main view 
allows the sales team to perform filter queries on the data. It would then display the information of attorney firms 
that fit these criteria. The sales person has the option to email the generic email of the company (info@company.com) or
to dive into the attorneys view of that firm to send more customized emails (these usually have a higher reply
rate). Once on this view, they are given the option to draft a template and send the email. Once sent, the email won't 
be emailed for testing purposes. It would be sent to our mailer instance for checking.
### SMTP/Mailer
For testing purposes and in order to avoid emailing attorneys before we're ready to go live, I decided to use mailhog. 
Mailhog is an email testing tool that mimics an SMTP server. Instead of actually sending emails, it provides a UI for  
the user to check the subject of emails sent, their destination and other emails related fields.
## Installation
1. Clone this repo into your computer.
2. If you are planning on running this application, you would need to set up some environment variables first. To set 
   up the environment variables please edit the values in `config/.env.dev`.
   2.1) You need to generate `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID` with permissions to write to S3 and to SQS.
   The rest are already configured with default placeholders.
3. Once the environments variables are properly set, you can run the 4 services using
   >$ docker-compose --env-file ./config/.env.dev up 
4. Visit `http://localhost:8000` to view the app
5. Visit `https://localhost:8025` to view the mailhog server
## Disclaimer
This is a beta project developed over the weekend. There's plenty of room for improvements in each service. To name a 
few:
- [ ] add rotating proxies to scraper to avoid being blocked
- [ ] tap into third party sources to augment the data for attorneys. (rocketreach, clearbit)
- [ ] validate emails of attorneys to avoid having a high bounce rate
- [ ] integrate with a robinai's CRM to track the progress of customers, and the emails we sent them
- [ ] improve front end of the webapp to add more features and allow for smoother user experience