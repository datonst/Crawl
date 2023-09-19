from playwright.sync_api import sync_playwright
import time
import os
import asyncio,aiofiles
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright
import pandas as pd
#source block image https://www.zenrows.com/blog/blocking-resources-in-playwright#function-handler
#async compare to synchronous https://www.youtube.com/watch?v=R4Oz8JUuM4s&t=1332s
excluded_resource_types = ["image"] 
invalid=['#','\\','<','$','+','%','>','!','`','&','*','\'','|','{','?','\"','=','}','/',':','@']
def block_aggressively(route): 
	if (route.request.resource_type in excluded_resource_types): 
		route.abort() 
	else: 
		route.continue_() 

async def async_block_aggressively(route): 
	if (route.request.resource_type in excluded_resource_types): 
		await route.abort() 
	else: 
		await route.continue_() 


def next_page(dem,page_competitions) :
    if(dem==0): return True
    try :
        page_competitions.locator('xpath=//*[@id="site-content"]/div[2]/div[5]/div/div/div/div[2]/i[2]').click(timeout=5000) #if bug time out raise timeout=30000
        return True
    except:
         print('Time out: Stop next page')
         return False

def main():
    with sync_playwright() as p:
        list_link=[]
        browser = p.chromium.launch(headless=True,slow_mo=50)
        open_broser = browser.new_context()
        # page_login = open_broser.new_page();
        # page_login.goto('https://www.kaggle.com/')
        page_competitions = open_broser.new_page()
        page_competitions.set_viewport_size({"width":1280,"height":1080})
        page_competitions.route("**/*", lambda route: block_aggressively(route))
        page_competitions.goto('https://www.kaggle.com/competitions')
        time.sleep(2); #wait page load
        page_competitions.locator('xpath=//*[@id="site-content"]/div[2]/div[4]/div/div[2]/div/div[1]/button[1]').click();

        # https://github.com/microsoft/playwright-python/issues/955
        # page_competitions.wait_for_load_state('networkidle')
        # t=0
        dem=0
        while (next_page(dem,page_competitions)==True) :
            dem+=1
            # t+=1
            # if(t>2): break
            # if(t<=18): continue
            # if (t>=20): break
            page_competitions.mouse.wheel(0,100)
            time.sleep(2)
            run=0
            while(run<20):
                try :
                    run+=1
                    # t+=1;
                    link=page_competitions.locator(f'xpath=//*[@id="site-content"]/div[2]/div[5]/div/div/div/ul/li[{run}]/div[1]/a').get_attribute('href',timeout=2000); #if bug time out raise timeout=3000
                    list_link.append('https://www.kaggle.com'+link)
                    # if(t>5): break
                except:
                    print('Time out: Done Page'+ str(run))
                    break
            # print(f"page {dem}: {run}")
        i=0
        for link in list_link:
            i+=1
            print(str(i)+': '+link)
    asyncio.run(run_page(list_link))
        
async def overview_page(page,newpath):
    try :
         await page.locator('xpath=//*[@id="pageheader-nav-item--overview"]').click(timeout=5000)
    except PlaywrightTimeoutError:
        await page.reload();
        try :    
            await page.locator('xpath=//*[@id="pageheader-nav-item--overview"]').click(timeout=5000)
        except:
             print(f"data_page {newpath}")
             return ["","",""]
    await page.mouse.wheel(0, 1000)
    # await page.check(selector='.sc-frtqox.ginvB',force=True)
    try :
         overview= await page.locator('xpath=//*[@id="abstract"]/div[1]').text_content(timeout=5000)
    except PlaywrightTimeoutError:
        await page.reload();
        try :    
            overview= await page.locator('xpath=//*[@id="abstract"]/div[1]').text_content(timeout=5000)
        except:
             overview=""
             print(f"data_page_overview {newpath}")
    
    try :
         description= await page.locator('xpath=//*[@id="description"]/div/div[2]/div/div').text_content(timeout=5000)
    except PlaywrightTimeoutError:
        await page.reload();
        try :    
            description= await page.locator('xpath=//*[@id="description"]/div/div[2]/div/div').text_content(timeout=5000)
        except:
             description=""
             print(f"data_page_description {newpath}")

    try :
        evaluation= await page.locator('xpath=//*[@id="evaluation"]/div/div[2]/div/div').text_content(timeout=5000)
    except:
        evaluation=""
        print(f"data_page_evaluation {newpath}")


    if (description or evaluation or overview) :
        html=await page.locator('xpath=/html').inner_html();
        async with aiofiles.open(f'{newpath}/overview.html', mode='w',encoding="utf-8") as f:
            await f.write(html)
            await f.close()
    return [overview,description,evaluation];
    # html= await page.locator('xpath=//*[@id="site-content"]/div[2]/div/div[2]').inner_html();

        

async def data_page(page,newpath):
    try :
         await page.locator('xpath=//*[@id="pageheader-nav-item--data"]').click(timeout=5000)
    except PlaywrightTimeoutError:
        await page.reload();
        try :    
            await page.locator('xpath=//*[@id="pageheader-nav-item--data"]').click(timeout=5000)
        except:
             print(f"data_page_not_found {newpath}")
             return ["",""]

    await page.mouse.wheel(0, 1000)
    # await page.wait_for_load_state('networkidle')
    try :
         dataset=await page.locator('xpath=//*[@id="site-content"]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]/div/div').text_content(timeout=5000)
    except PlaywrightTimeoutError:
        await page.reload();
        try :    
            dataset=await page.locator('xpath=//*[@id="site-content"]/div[2]/div/div[2]/div[1]/div[1]/div/div[2]/div/div').text_content(timeout=5000)
        except:
             dataset=""
             print(f"data_page_dataset {newpath}")
    
    try: 
        link_download= await page.locator('xpath=//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[2]/div/span').text_content(timeout=5000)
    except:
         link_download=""
         print(f"data_page_link_download {newpath}")
    # print (dataset)
    # print(link_download)
    if (dataset or link_download) :
        html=await page.locator('xpath=/html').inner_html();
        async with aiofiles.open(f'{newpath}/data.html', mode='w',encoding="utf-8") as f:
            await f.write(html)
            await f.close()       
    return [dataset,link_download]

    # html= await page.locator('xpath=//*[@id="site-content"]/div[2]/div/div[2]').inner_html();

async def code_page(page,newpath):
    try :
         await page.locator('xpath=//*[@id="pageheader-nav-item--code"]').click(timeout=5000)
    except PlaywrightTimeoutError:
        await page.reload();
        try :    
            await page.locator('xpath=//*[@id="pageheader-nav-item--code"]').click(timeout=5000)
        except:
             print(f"data_page code {newpath}")
             return ""
    await page.mouse.wheel(0, 100)
    
    totallink=""

    try :
         await page.get_by_role("button", name="Hotness arrow_drop_down").click(timeout=5000)
    except PlaywrightTimeoutError:
        await page.reload();
        try :    
            await page.get_by_role("button", name="Hotness arrow_drop_down").click(timeout=5000)
        except:
             print(f"data_page code {newpath}")

    try :
         await page.get_by_text("Most Votes").click(timeout=5000)
    except PlaywrightTimeoutError:
         print (f"Competiton has not Most Votes : {newpath}")
    
    for element in range(1,6):
        try :
            link=await page.locator(f'xpath=//*[@id="site-content"]/div[2]/div/div[2]/div[2]/div[1]/div/div[4]/div[2]/ul/li[{element}]/div[1]/a').get_attribute('href',timeout=5000)
            totallink= totallink + f"https://www.kaggle.com{link}\n"
        except:
            print(f'Code solutions are only {element} code {newpath}')
            break
    return totallink
    # html= await page.locator('xpath=//*[@id="site-content"]/div[2]/div/div[2]').inner_html();


async def run(playwright,list_link):
    create_chromium=playwright.chromium
    browser = await create_chromium.launch(headless=True,slow_mo=50)
    open_browser = await browser.new_context()
    page = await open_browser.new_page()
    await page.route("**/*", lambda route: async_block_aggressively(route)) 
    await page.set_viewport_size({"width":1280,"height":1080})
    dem=0
    list_data=[]
    for link in list_link: #vong for link list
        dem+=1
        await page.goto(link)
        try:
            name =await page.locator('xpath=//*[@id="site-content"]/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div[1]/h1').text_content(timeout=5000)
            name=name.strip()
            name=name.rstrip()
            for ch in invalid:
                 name=name.replace(ch,'')
        except PlaywrightTimeoutError:
             name=""
             print(f"{dem} :no_name")
        page_data= []
        newpath = f"D:/Crawl_HTML/{dem}.{name}" 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        page_data.append(dem)
        page_data.append(name);
        overview=await overview_page(page,newpath)
        for data in overview :
             page_data.append(data)
        data_= await data_page(page,newpath)
        for data in data_:
             page_data.append(data)
        totallink=await code_page(page,newpath)
        page_data.append(totallink)
        list_data.append(page_data)
    df= pd.DataFrame(list_data,columns=["Id","Name","Overview","Description","Evaluation","Dataset","Download","Most Votes"])
    df.to_excel("results.xlsx",header=True,index=False,engine='xlsxwriter') #Một vài kí tự đặc biệt không hợp lệ excel
    await browser.close()

async def run_page(list_link):
    async with async_playwright() as playwright: # or "firefox" or "webkit".
        await run(playwright,list_link)
    


main()


    