import sqlite3

DATABASE_PATH = "data/database"

def connect():
    '''Open a connection to the database'''
    conn = sqlite3.connect(DATABASE_PATH)
    conn.execute("PRAGMA foreign_keys = ON") # Enable foreign key suports
    return conn

def insert_protection_curve(name, protection_type, curve_type):
    '''Insert a new curve into protection_curves. Return the new curve_id'''

def insert_discrete_points(curve_id, points):
    '''Insert multiple data points into discrete_overcurrent_curves'''

def insert_equation(curve_id, formula):
    '''Insert a formula into equation_overcurrent_curves'''

def get_all_curves():
    '''Return a list of all saved curves (id, name, type)'''

def get_curve_by_id(curve_id):
    '''Return the full curve data (metadata + points or formula)'''

def delete_curve(curve_id):
    '''Detele a curve and its associate data'''