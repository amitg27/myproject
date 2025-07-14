from playwright.sync_api import sync_playwright

def scrape_naukri_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Go to the ASP.NET jobs page
        page.goto("https://www.naukri.com/asp-dot-net-jobs", timeout=60000)
        page.wait_for_timeout(5000)  # wait for page to load properly

        jobs = page.locator('div.srp-jobtuple-wrapper')  # all job cards

        job_data = []

        for i in range(jobs.count()):
            job = jobs.nth(i)
            
            try:
                title_element = job.locator('a.title').first
                title = title_element.text_content().strip()
                detail_url = title_element.get_attribute('href')
            except:
                title = None

            try:
                employer = job.locator('a.comp-name').first.text_content().strip()
            except:
                employer = None

            try:
                description = job.locator('span.job-desc').first.text_content().strip()
            except:
                description = None
            
            try:
                location = job.locator('span.locWdth').first.text_content().strip()
            except:
                location = ""

            try:
                experience = job.locator('span.expwdth').first.text_content().strip()
            except:
                experience = ""

            job_data.append({
                'title': title,
                'employer': employer,
                'description': description,
                'detail_url': detail_url,
                'location':location,
                'experience': experience

            })

        browser.close()
        return job_data

# Run and print data
if __name__ == "__main__":
    jobs = scrape_naukri_jobs()
    for idx, job in enumerate(jobs, start=1):
        print(f"{idx}. Job Title: {job['title']}")
        print(f"Employer: {job['employer']}")
        print(f"Location: {job['location']}")
        print(f"   Experience: {job['experience']}")
        print(f"Description: {job['description']}")
        print(f"Detail URL: {job['detail_url']}")
        print("-" * 80)
