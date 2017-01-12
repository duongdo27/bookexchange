import sqlite3
from selenium import webdriver
from lxml import html
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep


class Loader(object):
    def __init__(self):
        self.conn = sqlite3.connect('../db.sqlite3')
        self.cursor = self.conn.cursor()
        #self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS()
        self.url = "http://bookstore.csbsju.edu/sjub/buy_textbooks.asp?"

    def get_or_create_section(self, section_data):
        query = "insert or ignore into textbook_section (department, course, section, professor) values (?, ?, ?, ?)"
        self.cursor.execute(query, section_data)
        self.conn.commit()
    
        query = "select id from textbook_section where department = ? and course = ? and section = ?"
        self.cursor.execute(query, (section_data[0], section_data[1], section_data[2]))
    
        result = self.cursor.fetchone()
        return result[0]

    def get_or_create_book(self, book_data):
        query = "insert or ignore into textbook_book (name, isbn, author) values (?, ?, ?)"
        self.cursor.execute(query, book_data)
        self.conn.commit()
    
        query = "select id from textbook_book where isbn = ?"
        self.cursor.execute(query, (book_data[1],))
    
        result = self.cursor.fetchone()
        return result[0]

    def load_data(self, section_data, books_data):
        section_id = self.get_or_create_section(section_data)
    
        query = "delete from textbook_booksection where section_id = ?"
        self.cursor.execute(query, (section_id,))
        self.conn.commit()
    
        for book_data in books_data:
            book_id = self.get_or_create_book(book_data)
            query = "insert or ignore into textbook_booksection (section_id, book_id) values (?, ?)"
            self.cursor.execute(query, (section_id, book_id,))
            self.conn.commit()

    def wait_for_id(self, the_id, timeout=3):
        element_present = EC.presence_of_element_located((By.ID, the_id))
        WebDriverWait(self.driver, timeout).until(element_present)
        sleep(1)

    def find_section_books(self, dept_num, course_num, section_num):
        print 'Dept: {}. Course: {}. Section: {}'.format(dept_num, course_num, section_num)
        self.driver.get(self.url)
        self.wait_for_id('fTerm')

        self.driver.find_element_by_xpath('//select[@id="fTerm"]/option[3]').click()
        self.wait_for_id('fDept')
        try:
            self.driver.find_element_by_xpath('//select[@id="fDept"]/option[{}]'.format(dept_num)).click()
        except NoSuchElementException:
            return

        self.wait_for_id('fCourse')
        try:
            self.driver.find_element_by_xpath('//select[@id="fCourse"]/option[{}]'.format(course_num)).click()
        except NoSuchElementException:
            self.find_section_books(dept_num + 1, 2, 2)
            return

        self.wait_for_id('fSection')
        try:
            self.driver.find_element_by_xpath('//select[@id="fSection"]/option[{}]'.format(section_num)).click()
        except NoSuchElementException:
            self.find_section_books(dept_num, course_num + 1, 2)
            return

        self.wait_for_id('tbe-add-section')
        self.driver.find_element_by_id('tbe-add-section').click()

        self.wait_for_id('generate-book-list')
        self.driver.find_element_by_id('generate-book-list').click()

        self.read_current_page()
        self.find_section_books(dept_num, course_num, section_num + 1)

    def read_current_page(self):
        self.wait_for_id('course-bookdisplay-coursename')
        page_source = self.driver.page_source
        tree = html.fromstring(page_source)

        info = tree.xpath('//span[@id="course-bookdisplay-coursename"]/text()')[0]
        info_ls = info.split(" ")
        department = info_ls[0]
        course = info_ls[2].replace(',', '')
        section = info_ls[4]
        professor = info_ls[6].replace(')', '') + ' ' + info_ls[5].replace('(', '').replace(',', '')
        section_data = (department, course, section, professor)

        book_elements = tree.xpath('//tr[@class="book course-required"]') + \
            tree.xpath('//tr[@class="book course-required alt"]')

        books_data = []
        for book_element in book_elements:
            name = book_element.xpath('.//span[@class="book-title"]/text()')[0]

            isbn_ls = book_element.xpath('.//span[@class="isbn"]/text()')
            if isbn_ls:
                isbn = isbn_ls[0]
            else:
                continue
            author_ls = book_element.xpath('.//span[@class="book-meta book-author"]/text()')
            if author_ls:
                author = author_ls[0]
            else:
                author = ''
            books_data.append((name, isbn, author))

        self.load_data(section_data, books_data)

    def run(self):
        try:
            self.find_section_books(3, 2, 2)
        finally:
            self.conn.close()
            self.driver.close()


if __name__ == '__main__':
    Loader().run()
