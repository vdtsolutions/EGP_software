import base64
import os
from string import Template
import pdfkit
import Components.config as Config
import Components.logger as logger


def img_to_base64(url):
    try:
        with open(url, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
        my_string = "data:image/png;base64," + my_string.decode('utf-8')
        return my_string
    except:
        pass


header = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <title>Bootstrap Example</title>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
            
             <style>
      .pageA4 {
        page-break-before: always;
        height: 29.7cm;
      }
    </style>
            </head>
            <body>
        """

footer = "</body> </html>"

img_template = Template("""
    <div class="container pageA4">
       <div class="row">
       
      <div class="col-md-12" style="display: inline-block; overflow: auto">
       <img src="$img"  class="mx-auto d-block"
            style="height: 100%"
       />
         <br />
          <b class="float-right">Length : 13m</b>
      </div>        
       </div>
    </div>
""")


def generate_image_body(company_name, pipe_id, length, breadth):
    img_url = "./Charts/" + company_name + "/" + str(pipe_id) + ".png"
    img = img_to_base64(img_url)
    if img:
        return img_template.substitute(img=img, length=length, breadth=breadth)
    else:
        return "<div class='container pageA4'><b>Picture Not Found for Pipe Id : " + str(
            pipe_id) + "</b></div>"


def generate_table(data, pipe_id):
    head = "<div class='container pageA4'><div class='jumbotron text-center'><h1>Pipe ID :" + str(
        pipe_id) + "</h1> </div>"
    head += """
     <h2>Defect List :</h2>
        <br />
        <table class="table table-bordered text-center">
          <thead>
            <tr>
              <th>Defect Id</th>
              <th>Length</th>
              <th>Breadth</th>
              <th>Angle</th>
              <th>Depth</th>
            </tr>
          </thead>
          <tbody>
    """

    footer = """
    </tbody>
        </table>
    </div>
    """
    body = ""
    row = Template("""
            <tr>
                  <td>$id</td>
                  <td>$length</td>
                  <td>$breadth</td>
                  <td>$angle</td>
                  <td>$depth</td>
                </tr>""")
    for element in data:
        d = row.substitute(id=element[2], length=element[3], breadth=element[4], angle=element[5], depth=element[6])
        body += d
    return head + body + footer


def Sort_Tuple(tup):
    tup.sort(key=lambda x: x[1])
    return tup


def get_defect_data(runid):
    with Config.connection.cursor() as cursor:
        try:
            Fetch_defect_data = "select * from defectdetail where runid='%s' "
            cursor.execute(Fetch_defect_data, (int(runid)))
            allSQLRows = cursor.fetchall()
            defect_data = []
            for record in allSQLRows:
                defect_data.append(record)
            allSQLRows = []
            defect_data.sort(key=lambda x: x[1])
            return defect_data
        except:
            pass


def generate_page(defect, company_name, pipe_id):
    page = generate_table(defect, pipe_id)
    page += generate_image_body(company_name, pipe_id, 20, 20)
    return page


def generate(company_name, runid):
    company_name = company_name.text()
    defect_data = get_defect_data(runid)
    report = ""
    path = os.getcwd() + '\\Reports\\' + company_name
    try:
        os.makedirs(path)
    except OSError as error:
        print(error)
        pass
    d_list = []
    if defect_data:
        pipe_id = defect_data[0][1]
        for defect in defect_data:
            if defect[1] == pipe_id:
                d_list.append(defect)
            else:
                report += generate_page(d_list, company_name, pipe_id)
                d_list.clear()
                d_list.append(defect)
                pipe_id = defect[1]
        report += generate_page(d_list, company_name, pipe_id)

    else:
        Config.info_msg("No Defect record Found.", "")
        logger.log_info("Report Generation aborted. No Defect record Found for " + company_name)
        return
    f = open("./Reports/" + company_name + "/" + company_name + "_report.html", "w+")
    f.write(header + report + footer)
    f.close()
    path_wkthmltopdf = 'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit.from_file(input="./Reports/" + company_name + "/" + company_name + "_report.html",
                     output_path="./Reports/" + company_name + "/" + company_name + "_report.pdf",
                     configuration=config)
    Config.info_msg("Report generated Successfully", "")
