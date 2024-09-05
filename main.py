from flask import Flask 
from flask import render_template
from flask import request
import pandas as pd

api = open("api.txt", "r").read().split("=")[1].strip()
app = Flask(__name__, template_folder='.')
##@app.route('/')
##def index():
##    return render_template('main1.html')



def ppl(eth, min, max, emp): ####takes in the stats given in the text box


    # read in the original CSV file
        df = pd.read_csv("98-401-X2016041_English_CSV_data.csv", low_memory=False)

        pd.options.mode.chained_assignment = None


        ethnicity = eth

        min_population = int(min)

        max_population = int(max)

        min_employ = int(emp)


        # data validaiton
        if df.loc[df['DIM: Profile of Census Metropolitan Areas/Census Agglomerations (2247)'] == ethnicity].shape[0] == 0:
             # add ui displaying error in future, for now, i'll just break and print it
            print("not a valid country")
            raise Exception("Please enter a valid country")
             # other parameters will throw errors during type conversion if they aren't integers, good enough for now

        # select the specific columns that are relevant
        columns_to_keep = ['GEO_NAME', 'DIM: Profile of Census Metropolitan Areas/Census Agglomerations (2247)', 'Dim: Sex (3): Member ID: [1]: Total - Sex']
        new_df = df[columns_to_keep]


        # select the specific rows that are relevant
        ethnicitydf = new_df.loc[new_df['DIM: Profile of Census Metropolitan Areas/Census Agglomerations (2247)'] == ethnicity]

        populationdf = new_df.loc[new_df['DIM: Profile of Census Metropolitan Areas/Census Agglomerations (2247)'] == "Population, 2016"].drop("DIM: Profile of Census Metropolitan Areas/Census Agglomerations (2247)", axis=1)


        populationdf.rename(columns={'GEO_NAME': 'City/Town', 'Dim: Sex (3): Member ID: [1]: Total - Sex': 'Total Population'}, inplace=True)


        ethnicitydf.rename(columns={'GEO_NAME': 'City/Town', 'DIM: Profile of Census Metropolitan Areas/Census Agglomerations (2247)': 'Ethnicity', 'Dim: Sex (3): Member ID: [1]: Total - Sex': 'Population'}, inplace=True)


        employmentdf = new_df.loc[new_df['DIM: Profile of Census Metropolitan Areas/Census Agglomerations (2247)'] == "Employment rate"].drop("DIM: Profile of Census Metropolitan Areas/Census Agglomerations (2247)", axis=1)


        employmentdf.rename(columns={'GEO_NAME': 'City/Town', 'Dim: Sex (3): Member ID: [1]: Total - Sex': 'Rate'}, inplace=True)



        #type conversion
        pd.to_numeric(ethnicitydf.Population)
        ethnicitydf.Population = ethnicitydf.Population.astype(int)
        employmentdf['Rate'] = employmentdf['Rate'].astype('float')
        populationdf['Total Population'] = populationdf['Total Population'].astype('int')

        #filtering based on user inputs
        minimum_popdf = populationdf.loc[populationdf["Total Population"] > min_population]
        filtered_employmentdf = employmentdf.loc[employmentdf.Rate > min_employ]

        summeddf = ethnicitydf.groupby('City/Town').sum(numeric_only = True)

        sorted_populationdf = populationdf.sort_values(by='City/Town', ascending=True)

        #finds percentage of ethnicity compared to total population

        percent = []
        for i in range(len(list(summeddf["Population"]))):
            percent.append(list(summeddf["Population"])[i]/list(sorted_populationdf["Total Population"])[i]*100)


        sorted_populationdf["Percentage"] = percent


        sorted_sumdf = sorted_populationdf.sort_values(by='Percentage', ascending=False)



        mid_population_rangedf = sorted_sumdf.loc[sorted_sumdf["Total Population"] < max_population]



        final_filtered = mid_population_rangedf[mid_population_rangedf['City/Town'].isin(filtered_employmentdf['City/Town'])] #Filtering complete 



        print(final_filtered.iloc[0,0])
        return final_filtered.iloc[0,0]


# employrows2.head(10)

# employrows3 = employrows2.iloc[:, 0]

# employrows2.head(15)




city = "canada"  ###canada should be the first result since we are going to canada
google = f"https://www.google.com/maps/embed/v1/place?key={api}&q=" #the google link that allows a search for the best result

total = google + city 
print(total)

@app.route('/') ##spawns the website in the first loop
def main():
    return render_template('Official.html', value = total)

@app.route('/', methods=['GET', 'POST']) ##gets the result of the text box from HTML
def server():
    print(request.form)
    tag = request.form['tag']   ##takes in the strings
    tag1 = int(request.form["tag1"])
    tag3 = int(request.form["tag3"])
    tag2 = int(request.form["tag2"])
    print(tag, tag1, tag2)
    city = ppl(tag, tag1, tag3,tag2)  ##calls the function to find best city
    print(ppl(tag, tag1, tag3,tag2))
    total = google + city
    print(total)
    return render_template('official.html', value = total)  ##spawns the google map with the best result

def sub():
    return render_template('Official.html', value = total)

if __name__ == "__main__": ##basic setting
    app.run(debug=True)

tag = request.form['tag']
print(tag)

##@app.route('/')
##def main1(name=None):
##    return render_template('main1.html')


###to start program type into command prompt
###python main.py
###to stop type 
###ctrl + c
###start button does not work
