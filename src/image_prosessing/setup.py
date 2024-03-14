from setuptools import find_packages, setup

package_name = 'image_prosessing'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='nikolai',
    maintainer_email='nikolarn@stud.ntnu.no',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'canny_with_box = image_prosessing.canny_with_box:main',
            'canny_with_box_original = image_prosessing.canny_with_box_original:main',
            'Image_test = image_prosessing.Image_test:main',
            'blueye_image_yolo = image_prosessing.blueye_image_yolo:main',
            'yolo_chain_value = image_prosessing.yolo_chain_value:main',
            'threshold_with_box = image_prosessing.threshold_with_box:main',
        ],
    },
)
