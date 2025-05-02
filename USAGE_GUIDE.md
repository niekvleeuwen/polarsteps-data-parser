# Usage guide
Detailed step-by-step guide for non-programmers to install and use the polarsteps-data-parser program.

## Step 1: Install Python

The program requires Python. If you don’t have it installed:

1. Go to the official Python website: https://www.python.org/downloads/
1. Click Download Python (choose the latest version with a minium version of Python 3.11).
1. **IMPORTANT:** When installing, make sure to check the box that says
`Add Python to PATH` before clicking **Install Now**.

Once installed, you’re ready to install the polarsteps data parser.

## **Step 2: Open the Command Prompt (Terminal)**

* On **Windows**
  Press `Windows Key + R`, type `cmd`, and press **Enter**.

* On **Mac**
  Press `Command + Space`, type `Terminal`, and press **Enter**.

* On **Linux**
  Open the Terminal from your applications menu.

## **Step 3: Install the Program**

In the command prompt or terminal window, type this and press **Enter**:

```
pip install polarsteps-data-parser
```

You only have to do this once, it installs the tool onto your computer.

## **Step 4: Export Your Trip Data from Polarsteps**

You need the data from your Polarsteps trip.

1. Go to [Polarsteps.com](https://www.polarsteps.com/) and log in.
1. Click on your profile and go to the 'Account settings'.
1. Download the ZIP file via 'Download my data' in the Privacy section.
1. Go the the downloads folder on your computer and **extract** (right-click the ZIP file and choose **Extract All**).
1. Inside the newly created folder, there will be two folders: `trip` and `user`.
1. Navigate inside the `trip` folder and locate the trip you want to convert to a PDF (for example `guatemala_12345678`).

👉 Let’s say you extracted the folder to `Documents`. You will need to pass the following path to the program:

`C:\Users\YourName\Documents\PolarstepsTriptrip\guatemala_12345678` (Windows)

or

`/Users/YourName/Documents/PolarstepsTrip/trip/guatemala_12345678/` (Mac)


## **Step 5: Run the Program**

Back in your command prompt / terminal, navigate to where your trip folder is located.

### On **Windows**

```
cd "C:\Users\YourName\Documents"
```

### On **Mac/Linux**

```
cd /Users/YourName/Documents
```

Now run this command to generate the PDF:

```
polarsteps-data-parser "C:\Users\YourName\Documents\PolarstepsTriptrip\guatemala_12345678"
```

✅ This will create a PDF called **Trip report.pdf** inside the `Documents` folder (where you ran the command).

---

### **Optional: Customize the Output PDF Name**

If you want the PDF to have a custom name (for example, "Guatemala Trip.pdf"), run:

```
polarsteps-data-parser "<path>" --output "Guatemala Trip.pdf"
```

## **Step 6: Open and Enjoy Your Trip Report**

The program will create a **PDF** file, just open it like any regular document. You can view it, print it, or share it!

---

## **Troubleshooting**

* **Command not found?**
  Close the command prompt/terminal and open it again. Make sure Python is properly installed.

* **Missing files?**
  Ensure the folder has both `trip.json` and `locations.json`. The program needs both.

* **Program updates?**
  If you want to update the program later, simply run:

  ```
  pip install --upgrade polarsteps-data-parser
  ```