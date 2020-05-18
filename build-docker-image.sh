#!/usr/bin/env bash
echo "BUILDING IMAGES"
componentName="oco2peak"
componentVersion="0.0.1"
TAG="$componentName:$componentVersion"
echo "With tag $TAG"
docker build --tag $TAG .
echo "Done"