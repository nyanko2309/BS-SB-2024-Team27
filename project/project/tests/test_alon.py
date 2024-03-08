import unittest
from bs4 import BeautifulSoup


class TestPostRendering(unittest.TestCase):

    def setUp(self):
        # Mock HTML content for the homepage with two posts
        self.html_content = """
            <html>
                <body>
                    <div class="posts">
                        <div class="post">
                            <div class="post-info">
                                <div>Description: Post 1 Description</div>
                                <div>Location: Location 1</div>
                                <div>Work hours: 8 hours</div>
                                <div>Physical lvl: 3</div>
                                <div>Kind of job: Full-time</div>
                                <div>Category: Category 1</div>
                            </div>
                        </div>
                        <div class="post">
                            <div class="post-info">
                                <div>Description: Post 2 Description</div>
                                <div>Location: Location 2</div>
                                <div>Work hours: 6 hours</div>
                                <div>Physical lvl: 2</div>
                                <div>Kind of job: Part-time</div>
                                <div>Category: Category 2</div>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
        """

        # Parse HTML content using BeautifulSoup
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def test_post_rendering(self):
        # Find the container for posts
        posts_container = self.soup.find('div', class_='posts')

        # Ensure the container exists
        self.assertIsNotNone(posts_container)

        # Find all post elements
        post_elements = posts_container.find_all('div', class_='post')

        # Ensure the correct number of posts are rendered
        self.assertEqual(len(post_elements), 2)  # We expect 2 posts in the homepage


if __name__ == '__main__':
    unittest.main()
