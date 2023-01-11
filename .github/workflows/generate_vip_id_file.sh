
generate_default_vip_id_file() {
    local agent=$1
    local version=$2
    # rename identity file  if one exists
    if [ -f "IDENTITY" ]; then
      #  rename to what volttron-core will look for
      mv IDENTITY "$agent-$version-default-vip-id"
    elif ls -t -1 ${agent}-*-default-vip-id 1> /dev/null 2>&1; then
      # if no IDENTITY file exists check if agent-version-default-vip-id file exists of so rename file to right version
      # There should be only one file but in case there is more take the latest
      file_to_rename=$(ls -t -1 ${agent}-*-default-vip-id | head -n 1)

      #  rename to match the bumped version
      mv $file_to_rename ${agent}-${version}-default-vip-id
    fi
}

agent_name=$1
version=$2

if [ -z "$agent_name" ] || [ -z "$version" ]
then
  echo "Usage generate_vip_id_file <agent_name> <version>"
  exit 1
fi
generate_default_vip_id_file "$agent_name" "$version"
