# **Pocket Pro**
- A full stack web application for tracking, storing and reviewing golf scores and round data.

## **Description**
- Create a backend database in Django using Django REST Framework and Thunderclient to store round data.
- Create a frontend UI that allows user to create an account, sign in, sign out, keep their golf scores and view data from past rounds.

## **MVP**
- Create a backend database in Django using Django REST Framework and Thunderclient to store field data for:
	- Users
	- Courses
	- Rounds
	- Holes
	- Strokes
	- Swings
	- Putts

- Create a frontend UI that allows users to:
	- Create an account
	- Sign in to an account
	- Sign out of account
	- Create a new round
		- Choose a golf course
		- Select either a 9 or 18 hole round to play
	- Play a round
		- View the number, total distance and par for the current hole they are on
		- View current stroke count
		- View current score above or below par(+/-)
		- View and increment or decrement current swing count
			- Auto increments or decrements total stroke count
		- View and increment or decrement current putt count
            - Auto increments or decrements total stroke count
- View updating score card while playing
	- Store stroke, swing and putt values in database that correlates to specific round
	- View scores and key data from past rounds:
		- Course
		- Date
		- Total score
		- Score above or below par (+/-)
		- Total putts
		- Eagles, birdies, pars, bogies, bogies +
	- Filter and sort past rounds data based on key factors

#

## **Models/Fields**
**user**
- **id** integer
- **username** varchar
- **password** password
- **last_login** datetime
- **is_superuser** boolean
- **first_name** varchar
- **last_name** varchar
- **email** email
- **is_active** boolean
- **date_joined** datetime

**round**
- **id** integer
- **user_id** integer [fk]
- **course_id** integer [fk]
- **date** datetime
- **round_length** integer
- **total_score** integer

**hole_score**
- **id** integer
- **round_id** integer [fk]
- **hole_i**d integer [fk]
- **strokes** integer
- **swings** integer
- **putts** integer

**course**
- **id** integer
- **name** varchar
- **par** integer


**holes**
- **id** integer
- **course_id** integer [fk]
- **par** integer
- **distance** integer
- **number** integer

#

## **Atomic Design | React Components**
1) **Sign in page**
    - Sign In Header Text
    - Username Subheader Text
        - Username Input Field
    - Password Subheader Text
        - Password Input Field
    - Login Button
    - Create Account Button

2) **Create Account Page**
    - New Account Header Text
    - First Name Subheader Text
        - First Name Input Field
    - Last Name Subheader Text
        - Last Name Input Field
    - Email Subheader Text
        - Email Name Input Field
    - Username Subheader Text
        - Username Name Input Field
    - Password Subheader Text
        - Password Input Field
    - Create Account Button

3) **Main Menu Page**
    - Logo Header
    - New Round Button
    - Round History Button
    - Account Button
    - Sign Out Button

4) **New Round Setup Page**
    - Logo Header
    - Course Header Text
    - Golf Course Button
    - Golf Course Button
    - Golf Course Button
    - Round Length Header Text
    - 9 Hole Button
    - 18 Hole Button
    - Begin Round Button
    - Main Menu Button

5) **Round Page**
    - Hole Info Box
        - Hole Distance Text
        - Hole Number Text
        - Hole Par Text
    - Total Numbers Box
        - Distance Box
            - Distance Header Text
            - Distance Number Text
        - Total Strokes Box
            - Strokes Header Text
            - Current Stroke Number
        - Current Score Box
            - -/+ Header Text
            - Current Score Text
    - Total Swings Box
        - Swings Header Text
        - Decrement Button (-)
        - Swings Number
        - Increment Button (+)
    - Total Putts Box
        - Putts Header Text
        - Decrement Button (-)
        - Putts Number
        - Increment Button (+)
    - Scorecard
        - Front 9 Scorecard
            - Row of 11 boxes
                - 1-9 + front total par + empty box
            - Row of 11 boxes
                - empty (updates with GET as strokes POST to database)
        - Back 9 Scorecard
            - Row of 11 boxes
                - 10-18 + back total par + front and back total par
            - Row of 11 boxes
                - empty (updates with GET as strokes POST to database)
    - Complete Hole Button
    - Main Menu Button

6) **Round History Page**
    - Logo Header
    - Header Box
        - Round History Header Text
    - Single Round Box
        - Key Stats Box
            - Course Name Text
            - Round Date Text
            - Amount Over/Under Par Text
            - Total Putts Text
            - Total Score Text
        - Score Type Amount Box
            - Eagle Amount Text
            - Birdie Amount Text
            - Par Amount Text
            - Bogey Amount Text
            - Bogey+ Amount Text
        - Scorecard
            - Front 9 Scorecard
                - Row of 11 boxes
                    - 1-9 + front total par + empty box
                - Row of 11 boxes
                    - 1-9 stroke amounts + front total strokes amount + empty box
            - Back 9 Scorecard
                - Row of 11 boxes
                    - 10-18 stroke amounts + back total strokes amount + front and back total par
                - Row of 11 boxes
                    - 10-18 stroke amounts + back total strokes amount + front and back total strokes amount
    - Main Menu Button


#

## **Models**
### **Imports**

    from django.db import models
    from django.contrib.auth.models import AbstractUser
    from django.utils import timezone
    from django.config import settings

### **CustomUser**

    class CustomUser(AbstractUser):
        
        def __str__(self):
            return self.username

### **Course**

    class Course(models.Model):
        name = models.CharField(max_length=50)
        par = models.IntegerField()

        def __str__(self):
            return f'{self.name}, {self.par}'

### **Hole**

    class Hole(models.Model):
        course = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        par = models.IntegerField()
        distance = models.IntegerField()
        number = models.IntegerField()

        def __str__(self):
            return f'{self.course}, {self.par}, {self.distance}, {self.number}'


### **Round**

    class Round(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        course = models.ForeignKey('Course', on_delete=models.CASCADE)
        date = models.DateTimeField(default=timezone.now)
        round_length = models.IntegerField()
        total_score = models.IntegerField()

        def __str__(self):
            return f'{self.user}, {self.course}, {self.date}, {self.round_length}, {self.total_score}'

### **HoleScore**

    class HoleScore(models.Model):
        round = models.ForeignKey('Round', on_delete=models.CASCADE)
        hole = models.ForeignKey('Hole', on_delete=models.CASCADE)
        strokes = models.IntegerField()
        swings = models.IntegerField()
        putts = models.IntegerField()

        def __str__(self):
            return f'{self.round}, {self.hole}, {self.strokes}, {self.swings}, {self.putts}'

#

## **Serializers**


#

## **Views**


#

## **URLS**

#