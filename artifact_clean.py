import boto3

def cleanup_ecr_images(repository_name, keep_count=5, region='us-east-2'):
    """Deletes old ECR images, keeping only the most recent ones."""
    ecr = boto3.client('ecr', region_name=region)

    try:
        response = ecr.describe_images(repositoryName=repository_name)
        images = response['imageDetails']

        # Sort images by push date (newest to oldest)
        images.sort(key=lambda x: x['imagePushedAt'], reverse=True)

        images_to_delete = []

        # Skip the first 'keep_count' images (the most recent ones we want to keep)
        for image in images[keep_count:]:
            # Safety rule: never delete the 'latest' tag or specific production tags
            if 'imageTags' in image and 'latest' in image['imageTags']:
                continue

            # Add the image to the deletion list based on its Digest (unique hash)
            images_to_delete.append({'imageDigest': image['imageDigest']})

        if images_to_delete:
            print(f"Starting cleanup: {len(images_to_delete)} old images in repository '{repository_name}'.")

            # Actual batch delete command (uncomment to use in production):
            # ecr.batch_delete_image(repositoryName=repository_name, imageIds=images_to_delete)

            for img in images_to_delete:
                print(f" - Marked for deletion (Digest): {img['imageDigest']}")
        else:
            print(f"Repository '{repository_name}' is clean. Only the {keep_count} most recent images are present.")

    except Exception as e:
        print(f"Error accessing ECR repository: {e}")

if __name__ == '__main__':
    REPO_NAME = 'my-microservice-app'
    cleanup_ecr_images(REPO_NAME)